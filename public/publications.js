(() => {
  const root = document.querySelector(".publications-page");
  if (!root) return;
  const buttons = Array.from(root.querySelectorAll(".style-button"));
  const sentence = (value) => value && /[.!?]$/.test(value) ? value : `${value}.`;
  const formatCitation = (record, style) => {
    const { authors, title, details, year, number, gost } = record;
    if (style === "gost") return gost;
    if (style === "bibtex") return `@misc{antamoshkin${year}_${String(number).padStart(3, "0")},
  author = {${authors}},
  title = {${title}},
  year = {${year}},
  note = {${gost}}
}`;
    if (style === "apa") return `${authors} (${year}). ${sentence(title)} ${sentence(details)}`;
    if (style === "harvard") return `${authors} ${year}. ${sentence(title)} ${sentence(details)}`;
    if (style === "ieee") return `[${number}] ${authors}, "${title}," ${sentence(details)}`;
    if (style === "vancouver") return `${sentence(authors)} ${sentence(title)} ${sentence(details)} ${year}.`;
    return `${sentence(authors)} "${title}." ${sentence(details)} ${year}.`;
  };
  const updateCitations = (style) => {
    root.querySelectorAll("[data-bibliography]").forEach((citation) => {
      const record = JSON.parse(citation.dataset.bibliography);
      citation.textContent = formatCitation(record, style);
      citation.dataset.citationStyle = style;
      citation.classList.toggle("citation-bibtex", style === "bibtex");
    });
  };
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const style = button.dataset.style;
      root.dataset.style = style;
      updateCitations(style);
      buttons.forEach((item) => {
        const active = item === button;
        item.classList.toggle("active", active);
        item.setAttribute("aria-pressed", active ? "true" : "false");
      });
    });
  });
})();
