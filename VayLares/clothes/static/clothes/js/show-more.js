const start = 9;
let items = 9;
function handler() {
  items += 3;
  const array = Array.from(document.querySelector('.flex-container').children);
  const visibleItems = array.slice(0, items);
  const productsLength = document.querySelectorAll('.product-flex-item').length;
  const showMore = document.querySelector('.show-more');
  visibleItems.forEach(el => el.classList.add('is-visible'));

  if (visibleItems.length === productsLength){
    showMore.style.display = 'none';
  }
}

window.onload=function(){
  const showMore = document.querySelector('.show-more');
  const productsLength = document.querySelectorAll('.product-flex-item').length;
  if (productsLength > start){
    showMore.style.display = '';
    showMore.addEventListener('click', handler);
  }
}
