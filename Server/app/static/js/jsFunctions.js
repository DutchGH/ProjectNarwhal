function changeCards(item){
  document.getElementById("titleBox").innerHTML = item[0];
  document.getElementById("tutorBox").innerHTML = item[1];
  document.getElementById("test5").innerHTML = item[2];
  document.getElementById("buildingBox").innerHTML = item[3];
  document.getElementById("cardImage").src = item[4];
  document.getElementById("cancelClass").href = "/function/cancel/" + item[5];
}
