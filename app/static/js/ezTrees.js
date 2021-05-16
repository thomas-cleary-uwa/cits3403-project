function sendToPage(url) {
  window.location.href = url;
}

function showDiv(divName) {
  var x = document.getElementsByClassName("hideable");
  var i;
  for (i = 0; i < x.length; i++){
      if (x[i].id == divName){
          x[i].style.display = "block";
      }
      else {
          x[i].style.display = "none";
      }
  }
}


