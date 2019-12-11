var dropdownUser = document.querySelector('#dropdown-user');
dropdownUser.addEventListener('click', function(event) {
  event.stopPropagation();
  dropdownUser.classList.toggle('is-active');
});