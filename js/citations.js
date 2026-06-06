document.addEventListener("DOMContentLoaded", () => {
  const refs = document.querySelectorAll(".references li");

  refs.forEach((ref, index) => {
    const number = index + 1;
    const refId = ref.id;

    const citations = document.querySelectorAll(`a.cite[href="#${refId}"]`);

    citations.forEach((cite, citeIndex) => {
      cite.textContent = `[${number}]`;
      cite.id = citeIndex === 0
        ? `cite-${refId}`
        : `cite-${refId}-${citeIndex + 1}`;
    });

    const backLink = document.createElement("a");
    backLink.href = citations[0] ? `#${citations[0].id}` : "#";
    backLink.textContent = `[${number}] `;
    backLink.className = "ref-backlink";

    ref.prepend(backLink);
  });
});