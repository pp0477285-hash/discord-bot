document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".button");
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      button.classList.add("is-active");
    });
  });
});
