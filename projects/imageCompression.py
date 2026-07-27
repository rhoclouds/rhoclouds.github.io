# made by rhoclouds

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps


# ------------------------------------------------------------
# Load and resize the image
# ------------------------------------------------------------

script_folder = Path(__file__).resolve().parent
image_path = script_folder / "starry_night.jpg"

if not image_path.exists():
    raise FileNotFoundError(
        f"Could not find {image_path}. Place the image in the same folder "
        "as this notebook or change image_path."
    )

image = ImageOps.exif_transpose(Image.open(image_path)).convert("RGB")

# Keep the calculation manageable while preserving the aspect ratio.
image.thumbnail((640, 640), Image.Resampling.LANCZOS)

A = np.asarray(image, dtype=np.float64) / 255.0
m, n, channels = A.shape

print(f"Image dimensions: {m} × {n}")
print(f"Original RGB storage: {3 * m * n:,} numerical values")


# ------------------------------------------------------------
# Compute one SVD for each RGB channel
# ------------------------------------------------------------

channel_svd = []

for channel in range(channels):
    U, singular_values, Vt = np.linalg.svd(
        A[:, :, channel],
        full_matrices=False
    )
    channel_svd.append((U, singular_values, Vt))


# ------------------------------------------------------------
# Construct the rank-k approximation
# ------------------------------------------------------------

def truncated_svd_image(k):
    """Return the rank-k approximation of each RGB channel."""

    if not 1 <= k <= min(m, n):
        raise ValueError(f"k must satisfy 1 <= k <= {min(m, n)}.")

    approximation = np.empty_like(A)

    for channel, (U, singular_values, Vt) in enumerate(channel_svd):
        U_k = U[:, :k]
        S_k = singular_values[:k]
        Vt_k = Vt[:k, :]

        approximation[:, :, channel] = (
            (U_k * S_k) @ Vt_k
        )

    return np.clip(approximation, 0.0, 1.0)


def relative_frobenius_error(k):
    """Compute ||A - A_k||_F / ||A||_F using the discarded singular values."""

    discarded_energy = sum(
        np.sum(singular_values[k:] ** 2)
        for _, singular_values, _ in channel_svd
    )

    total_energy = sum(
        np.sum(singular_values ** 2)
        for _, singular_values, _ in channel_svd
    )

    return np.sqrt(discarded_energy / total_energy)


def theoretical_storage_fraction(k):
    """
    Compare the SVD storage 3k(m+n+1) with the original RGB storage 3mn.
    The factor of 3 cancels.
    """

    return k * (m + n + 1) / (m * n)


# ------------------------------------------------------------
# Compare several approximation ranks
# ------------------------------------------------------------

candidate_ranks = [5, 15, 40, 80]
ranks = [k for k in candidate_ranks if k <= min(m, n)]

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 13
})

figure, axes = plt.subplots(
    1,
    len(ranks) + 1,
    figsize=(4.1 * (len(ranks) + 1), 5),
    constrained_layout=True
)

for axis, k in zip(axes[:-1], ranks):
    A_k = truncated_svd_image(k)
    error = relative_frobenius_error(k)
    storage = theoretical_storage_fraction(k)

    axis.imshow(A_k)
    axis.set_title(
        f"Rank {k}\n"
        f"Error: {100 * error:.1f}%   "
        f"Storage: {100 * storage:.1f}%"
    )
    axis.axis("off")

axes[-1].imshow(A)
axes[-1].set_title(f"Original\n{m} × {n}")
axes[-1].axis("off")

plt.show()


# ------------------------------------------------------------
# Numerical summary
# ------------------------------------------------------------

print("\nApproximation summary")

for k in ranks:
    error = relative_frobenius_error(k)
    storage = theoretical_storage_fraction(k)

    print(
        f"Rank {k:>3}: "
        f"relative error = {100 * error:>5.1f}%   "
        f"theoretical storage = {100 * storage:>5.1f}%"
    )


# ------------------------------------------------------------
# Estimate the effective rank
# ------------------------------------------------------------

component_energy = sum(
    singular_values ** 2
    for _, singular_values, _ in channel_svd
)

cumulative_energy = (
    np.cumsum(component_energy) / np.sum(component_energy)
)

for target in [0.90, 0.95, 0.99]:
    effective_rank = np.searchsorted(cumulative_energy, target) + 1

    print(
        f"Rank needed to retain {100 * target:.0f}% "
        f"of the singular-value energy: {effective_rank}"
    )