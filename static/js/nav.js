var lineOne = document.getElementsByClassName('nav-line1')[0];
var lineTwo = document.getElementsByClassName('nav-line2')[0];
var lineThree = document.getElementsByClassName('nav-line3')[0];
var navigation = document.getElementsByClassName('nav-all')[0];

document.getElementsByClassName('nav-box')[0].onclick = 
  function() {
    // open the nav
    if (this.classList.contains('close')){
      lineOne.classList.add('open');
      lineTwo.classList.add('open');
      lineThree.classList.add('open');
      navigation.classList.remove('close');
      navigation.classList.add('open');
      this.classList.remove('close');
      this.classList.add('open'); 
    } else {
    // close the nav
      lineOne.classList.remove('open');
      lineTwo.classList.remove('open');
      lineThree.classList.remove('open');
      navigation.classList.remove('open');
      navigation.classList.add('close');
      this.classList.remove('open');
      this.classList.add('close'); 
    }
  }
