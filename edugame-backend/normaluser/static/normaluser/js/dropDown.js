console.log(`Hello`);

let dropHeading = document.querySelector(`.searchHeading`);
let submenu = document.querySelector(`.subMenu`);
let arrow = document.querySelector(`#icon`);

function show() {
  submenu.classList.add(`active`);
  arrow.classList.add(`rotate`);

  //   For Manually removing the submenu
  dropHeading.addEventListener(`click`, hide);

  //   For automatic removing the submenu
  setTimeout(() => {
    console.log(`bxsjxb`);
    hide();
  }, 4000);
}

function hide() {
  submenu.classList.remove(`active`);
  arrow.classList.remove(`rotate`);
  dropHeading.removeEventListener(`click`, hide);
}

dropHeading.addEventListener(`click`, show);
