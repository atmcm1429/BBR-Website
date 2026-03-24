(function () {
  const currentYear = String(new Date().getFullYear());

  document.querySelectorAll("[data-current-year]").forEach((node) => {
    node.textContent = currentYear;
  });

  const legacyYear = document.getElementById("y");
  if (legacyYear && !legacyYear.textContent) {
    legacyYear.textContent = currentYear;
  }

  initHamburgerMenu();
  initLazyEmbeds();
})();

function initHamburgerMenu() {
  const button = document.querySelector(".hamburger");
  const menu = document.getElementById("site-menu");

  if (!button || !menu) {
    return;
  }

  const closeMenu = () => {
    menu.classList.remove("open");
    button.classList.remove("active");
    button.setAttribute("aria-expanded", "false");
  };

  const toggleMenu = () => {
    const isOpen = menu.classList.toggle("open");
    button.classList.toggle("active", isOpen);
    button.setAttribute("aria-expanded", String(isOpen));
  };

  button.addEventListener("click", toggleMenu);

  document.addEventListener("click", (event) => {
    if (!menu.contains(event.target) && !button.contains(event.target)) {
      closeMenu();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeMenu();
    }
  });

  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });
}

function initLazyEmbeds() {
  const lazyEmbeds = document.querySelectorAll(
    "iframe[data-src], object[data-data], img[data-src]"
  );

  if (!lazyEmbeds.length) {
    return;
  }

  const loadEmbed = (element) => {
    if (element.dataset.src && !element.getAttribute("src")) {
      element.setAttribute("src", element.dataset.src);
      element.removeAttribute("data-src");
    }

    if (element.dataset.data && !element.getAttribute("data")) {
      element.setAttribute("data", element.dataset.data);
      element.removeAttribute("data-data");
    }
  };

  if (!("IntersectionObserver" in window)) {
    lazyEmbeds.forEach(loadEmbed);
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        loadEmbed(entry.target);
        observer.unobserve(entry.target);
      });
    },
    { rootMargin: "300px 0px" }
  );

  lazyEmbeds.forEach((element) => observer.observe(element));
}
