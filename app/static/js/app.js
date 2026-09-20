document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    document.querySelectorAll(".alert").forEach(el => {
      el.style.transition = "opacity .4s";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 500);
    });
  }, 4500);

  document.querySelectorAll("[data-slideshow]").forEach((slideshow) => {
    const slides = [...slideshow.querySelectorAll(".simhastha-slide")];
    const dots = [...slideshow.querySelectorAll(".slideshow-dots button")];
    let current = 0;
    let timer;

    const showSlide = (index) => {
      current = (index + slides.length) % slides.length;
      slides.forEach((slide, slideIndex) => slide.classList.toggle("active", slideIndex === current));
      dots.forEach((dot, dotIndex) => dot.classList.toggle("active", dotIndex === current));
    };

    const restart = () => {
      window.clearInterval(timer);
      timer = window.setInterval(() => showSlide(current + 1), 5000);
    };

    dots.forEach((dot, index) => dot.addEventListener("click", () => { showSlide(index); restart(); }));
    restart();
  });

  const widget = document.querySelector(".assistant-widget");
  if (!widget) return;

  const toggle = widget.querySelector(".assistant-toggle");
  const panel = widget.querySelector(".assistant-panel");
  const close = widget.querySelector(".assistant-close");
  const form = widget.querySelector(".assistant-form");
  const input = form.querySelector("input");
  const messages = widget.querySelector(".assistant-messages");
  const getSavedLocation = () => {
    try {
      const location = JSON.parse(localStorage.getItem("simhasthaUserLocation"));
      return location && typeof location.latitude === "number" && typeof location.longitude === "number" ? location : null;
    } catch (error) {
      return null;
    }
  };

  const setOpen = (open) => {
    panel.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
    if (open) input.focus();
  };

  const addMessage = (text, kind) => {
    const message = document.createElement("div");
    message.className = `assistant-message assistant-message-${kind}`;
    message.textContent = text;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
  };

  const ask = async (text) => {
    addMessage(text, "user");
    try {
      const response = await fetch("/assistant", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message: text, location: getSavedLocation() }) });
      if (!response.ok) throw new Error("Assistant unavailable");
      const data = await response.json();
      addMessage(data.answer, "bot");
      if (data.links?.length) {
        const links = document.createElement("div");
        links.className = "assistant-links";
        data.links.forEach((item) => {
          const link = document.createElement("a");
          link.href = item.url;
          link.textContent = item.label;
          links.appendChild(link);
        });
        messages.appendChild(links);
      }
    } catch (error) {
      addMessage("I could not connect right now. Please use the navigation above for help.", "bot");
    }
  };

  toggle.addEventListener("click", () => setOpen(panel.hidden));
  close.addEventListener("click", () => setOpen(false));
  widget.querySelectorAll(".assistant-suggestions button").forEach((button) => button.addEventListener("click", () => ask(button.textContent)));
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    ask(text);
  });

  window.addEventListener("simhastha:location", () => {
    const note = widget.querySelector(".assistant-note");
    if (note) note.textContent = "स्थान उपलब्ध है। आसपास की जानकारी पूछें; निर्देशांक सहेजे नहीं जाते।";
  });
});
