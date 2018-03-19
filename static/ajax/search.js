function search(model) {
   var query = document.getElementById("searchtext").value;
   var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("content").innerHTML = this.responseText
    }
  };
  xhttp.open("GET", ("/panda/search/" + model + "?query=" + query + ""), true);
  xhttp.send();
}