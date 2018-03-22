function add(slug) {
   var gameList = document.getElementById("recommending");
   var recGame = gameList.options[gameList.selectedIndex].value;
   var xhttp = new XMLHttpRequest();
   xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("RecommendGame").innerHTML =
      this.responseText;
      updateGameList(slug)
    }
  };
  xhttp.open("GET", ("/panda/game/" + slug + "/recommend?suggestion=" + recGame + ""), true);
  xhttp.send();
}

function updateGameList(slug) {
   var xhttp = new XMLHttpRequest();
   xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("options").innerHTML =
      this.responseText;
    }
  };
  xhttp.open("GET", ("/panda/game/" + slug + "/update"), true);
  xhttp.send();
}