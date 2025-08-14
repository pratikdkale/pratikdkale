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