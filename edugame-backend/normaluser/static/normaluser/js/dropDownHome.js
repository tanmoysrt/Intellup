const Menu = document.querySelector(".Menu");

const hamburger = document.querySelector(`.toggler`);

hamburger.addEventListener(`click`, () => {
  if (hamburger.checked) {
    Menu.style.top = "0";
    Menu.style.opacity = ".8";
    console.log(`checked`);
  } else {
    Menu.style.top = "-100%";
    console.log(`unchecked`);
    Menu.style.opacity = "0";
  }
});

let btn = document.querySelectorAll(`.qnaHeading`);

btn.forEach(function (button, index) {
  button.addEventListener(`click`, function () {
    console.log(`Clicked buttn ${index + 1}`);

    let content = button.nextElementSibling;
    console.log(content);

    if (JSON.stringify(button.classList).includes(`active`)) {
      button.classList.remove(`active`);
      button.nextElementSibling.classList.remove(`qnaactive`);
    } else {
      button.classList.add(`active`);
      button.nextElementSibling.classList.add(`qnaactive`);
    }
  });
});
