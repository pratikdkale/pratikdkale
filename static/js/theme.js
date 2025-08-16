(function(){
  const key = "theme";
  const root = document.documentElement;
  const preferred = localStorage.getItem(key);
  if (preferred) root.setAttribute("data-theme", preferred);
  const btn = document.getElementById("themeToggle");
  function updateIcon(){
    btn.textContent = root.getAttribute("data-theme")==="dark" ? "☾" : "☼";
  }
  updateIcon();
  btn.addEventListener("click", ()=>{
    const next = root.getAttribute("data-theme")==="dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    localStorage.setItem(key, next);
    updateIcon();
  });
})();

// ------------------ Mobile nav toggle ------------------
const burger = document.getElementById('navBurger');
const navBottom = document.getElementById('navBottom');

if (burger && navBottom) {
  burger.addEventListener('click', () => {
    const open = navBottom.getAttribute('data-open') === 'true';
    navBottom.setAttribute('data-open', String(!open));
    burger.setAttribute('aria-expanded', String(!open));
  });

  // Close menu after clicking a link
  navBottom.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      navBottom.setAttribute('data-open', 'false');
      burger.setAttribute('aria-expanded', 'false');
    });
  });
}
