//Search results for model provided (Game or Player
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

//Load players with given condition e.g all, competitive etc
function loadPlayers(game, types) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("content").innerHTML =
      this.responseText;
    }
  };
  xhttp.open("GET", ("/panda/game/"+ game + "/players?type=" + types +""), true);
  xhttp.send();
}

//Clear search results
function hide() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("content").innerHTML =
          "";
    }
  };
  xhttp.open("GET", '/panda/reset/', true);
  xhttp.send();
}