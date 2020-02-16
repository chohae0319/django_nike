const open = document.getElementById("signOpen");
const close = document.getElementById("signClose");
const modal = document.querySelector(".modal-wrapper");

open.onclick = () => {
  modal.style.display = "flex";
};

close.onclick = () => {
  modal.style.display = "none ";
};
