function changeCards(item){
  document.getElementById("titleBox").innerHTML = item[0];
  document.getElementById("tutorBox").innerHTML = item[1];
  document.getElementById("test5").innerHTML = item[2];
  document.getElementById("buildingBox").innerHTML = item[3];
  document.getElementById("cardImage").src = item[4];
  document.getElementById("cancelClass").href = "/function/cancel/" + item[5];
  document.getElementById("remindClass").href = "/function/remind/" + item[5];
}

function hideItems(course, pos, checkBox){
  var box = document.getElementById("browseBox");
  var rows = box.rows.length;
  for (var i = 0; i < rows;  i++) {
    var thisrow = box.rows[i]
    if(thisrow.cells[pos].innerHTML == course){
      if(checkBox.checked){
        if(thisrow.style.display != "none"){
          thisrow.style.display = "none";
        }
      }
      else{
          if(thisrow.style.display != "table-row"){
              thisrow.style.display = "table-row";
          }
      }
    }
  }
}
