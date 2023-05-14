const images_urls =  ['first.png', 'second.png', 'third.png', 'fourth.png', 'fifth.png']
var count = 1, c=4;
const names = ['one', 'two', 'three', 'four', 'five']
const statuses = [];


var timeout = window.setTimeout(first, timer());

function first() {
  window.clearTimeout(timeout);
  switcher(38);
  if(count == 6){
    document.getELementById('status').value = statuses;
    document.forms["myForm"].submit();
    // return 1;
}
}

function timer(){
  return 5000;
}


function switcher(casee) {
  switch (casee) {
    case 37:
     // alert('left key')
       statuses.push('rejected')
       document.getElementById('change-img').src = `/static/images/${images_urls[count]}`;
       document.getElementById('name').innerHTML = `${names[count]}`
       c = 4;
       count++;
       breaker();

       clearInterval(x);
       document.getElementById('time').innerHTML = '<p>5</p>';
       x = setInterval(function() {
        document.getElementById('time').innerHTML = `${c}`;
        c--;
      }, 1000);

       window.clearTimeout(timeout);
       timeout = window.setTimeout(first, timer());

       break;

    case 38:
      // alert('up key')
     statuses.push('no response ')
     document.getElementById('change-img').src = `/static/images/${images_urls[count]}`;
     document.getElementById('name').innerHTML = `${names[count]}`
     c = 4;
     count++;
     breaker();
     window.clearTimeout(timeout);
     timeout = window.setTimeout(first, timer());

     clearInterval(x);
     document.getElementById('time').innerHTML = '<p>5</p>';
     x = setInterval(function() {
      document.getElementById('time').innerHTML = `${c}`;
      c--;
    }, 1000);
    //  timeout = setTimeout(switcher(38), 5000);
     break;

    case 39:
      // alert('right key')
     statuses.push('accepted')
     document.getElementById('change-img').src = `/static/images/${images_urls[count]}`;
//     var img_src = document.getElementById("change-img").src;
//     alert(img_src);
     document.getElementById('name').innerHTML = `${names[count]}`;
     c = 4;
     count++;
     breaker();
     window.clearTimeout(timeout);
     timeout = window.setTimeout(first, timer());

     clearInterval(x);
     document.getElementById('time').innerHTML = '<p>5</p>';
     x = setInterval(function() {
      document.getElementById('time').innerHTML = `${c}`;
      c--;
    }, 1000);

    //  timeout = setTimeout(switcher(38), 5000);
       break;

 }
}

document.onkeydown = function(event) {
  key = event.keyCode
    switcher(key)
 };

function breaker() {
//alert(count);
  if(count >= 6 ){//&& (key == 37 || key == 38 || key == 39)){
    document.getElementById('status').value = statuses;
    document.forms["myForm"].submit();
    return;
  }
}



var x = setInterval(function() {
  document.getElementById('time').innerHTML = `${c}`;
  c--;
}, 1000);