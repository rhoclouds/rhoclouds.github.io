document.addEventListener("DOMContentLoaded", () => {
  function highlightElement(id) {
    const element = document.getElementById(id);
    if (element) {
      element.classList.add("highlight");
      setTimeout(() => element.classList.remove("highlight"), 1500);
    }
  }

  const refs = document.querySelectorAll(".references li");

  refs.forEach((ref, index) => {
    const number = index + 1;
    const refId = ref.id;
    const citations = document.querySelectorAll(`a.cite[href="#${refId}"]`);

    citations.forEach((cite, citeIndex) => {
      cite.textContent = `[${number}]`;
      cite.id = citeIndex === 0 ? `cite-${refId}` : `cite-${refId}-${citeIndex + 1}`;
    });

    const backLink = document.createElement("a");
    backLink.href = citations[0] ? `#${citations[0].id}` : "#";
    backLink.textContent = `[${number}]`;
    backLink.className = "ref-backlink";

    ref.prepend(document.createTextNode(" "));
    ref.prepend(backLink);
  });

  document.querySelectorAll('a[href^="#ref"], a[href^="#cite"]').forEach(link => {
    link.addEventListener("click", function () {
      const targetId = this.getAttribute("href").substring(1);
      highlightElement(targetId);
    });
  });
});