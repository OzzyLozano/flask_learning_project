const navbarBtn = document.getElementById('navbar-toggler')
const navbarContent = document.getElementById('navbar-content')
const navbarBtnUpperLine = document.querySelector('.navbar-btn__upper-line')
const navbarBtnBottomLine = document.querySelector('.navbar-btn__bottom-line')
let isNavbarOpen = false

navbarBtn.addEventListener('click', (e) => {
  if (!isNavbarOpen) openNavbar()
  else closeNavbar()
})
navbarContent.addEventListener('click', (e) => {
  if (isNavbarOpen) closeNavbar()
})

function openNavbar() {
  isNavbarOpen = true
  navbarContent.classList.add('open-navbar')
  navbarContent.classList.remove('close-navbar')
  navbarBtnUpperLine.classList.add('open')
  navbarBtnBottomLine.classList.add('open')
}
function closeNavbar() {
  isNavbarOpen = false
  navbarContent.classList.add('close-navbar')
  navbarContent.classList.remove('open-navbar')
  navbarBtnUpperLine.classList.remove('open')
  navbarBtnBottomLine.classList.remove('open')
}
