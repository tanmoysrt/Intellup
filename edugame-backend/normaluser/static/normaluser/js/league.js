console.log(`hello`);

let leagueName = document.getElementById(`LeagueName`);
let button = document.querySelectorAll(`.batch`);

function activate(type) {
  disable();
  switch (type) {
    case `bronze`:
      button[0].classList.add(`active`);
      leagueName.innerText = `Bronze League`;
      break;
    case `silver`:
      button[1].classList.add(`active`);
      leagueName.innerText = `Silver League`;
      break;
    case `gold`:
      button[2].classList.add(`active`);
      leagueName.innerText = `Gold League`;
      break;

    default:
      break;
  }
}

function disable() {
  button.forEach((Element) => {
    Element.classList.remove(`active`);
  });
}
