/* Progressive enhancements: all project content remains readable without JavaScript. */
const filterGroup = document.querySelector('.filters');
const projectCards = [...document.querySelectorAll('.project[data-category]')];
const projectPairs = [...document.querySelectorAll('.project-pair')];
const filterStatus = document.querySelector('#filter-status');

if (filterGroup && projectCards.length) {
  filterGroup.hidden = false;
  filterGroup.addEventListener('click', (event) => {
    const selected = event.target.closest('button[data-filter]');
    if (!selected) return;
    const category = selected.dataset.filter;
    filterGroup.querySelectorAll('button').forEach((button) => {
      const isSelected = button === selected;
      button.classList.toggle('active', isSelected);
      button.setAttribute('aria-pressed', String(isSelected));
    });
    projectCards.forEach((card) => {
      card.hidden = category !== 'all' && card.dataset.category !== category;
    });
    projectPairs.forEach((pair) => {
      pair.hidden = [...pair.querySelectorAll('.project')].every((card) => card.hidden);
    });
    const visible = projectCards.filter((card) => !card.hidden).length;
    filterStatus.textContent = `${visible} ${visible === 1 ? 'project' : 'projects'} shown.`;
  });
}

const copyButton = document.querySelector('.copy-email');
const copyStatus = document.querySelector('.copy-status');
if (copyButton && navigator.clipboard && window.isSecureContext) {
  copyButton.hidden = false;
  copyButton.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText('gqiang@uwo.ca');
      copyStatus.textContent = 'Email address copied.';
    } catch {
      copyStatus.textContent = 'Select and copy: gqiang@uwo.ca';
    }
  });
}

if ('IntersectionObserver' in window) {
  const navLinks = [...document.querySelectorAll('.site-header nav a')];
  const sectionObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      navLinks.forEach((link) => {
        if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }
  }, { rootMargin: '-10% 0px -65% 0px', threshold: 0 });
  document.querySelectorAll('section[id]').forEach((section) => sectionObserver.observe(section));
}
