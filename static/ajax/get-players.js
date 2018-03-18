function loadDoc(game) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("players").innerHTML =
      this.responseText;
    }
  };
  xhttp.open("GET", ("/panda/game/"+ game + "/players/"), true);
  xhttp.send();
}

function hideDoc(game) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("players").innerHTML =
          "";
    }
  };
  xhttp.open("GET", '/panda/player_xml_reset/', true);
  xhttp.send();
}