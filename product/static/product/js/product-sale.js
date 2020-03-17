$(function() {
  var gender = $("span#gender").text();
  $(`.${gender}`).addClass("select");
  //   현재 선택된 카테고리를 가져온다
  //    전체보기일 경우 category = ""
  var category = $("span#category").text();
  //   전체보기가 아니라면
  if (category.length) {
    //   category nav 바 목록을 가져와서
    var span = $("span.category");
    //  선택한 category 의 index 값과 맞추어서
    var selected = span[`${category - 1}`];
    //  className 추가
    selected.className = "underBar";
  }

  //   할인 가격 적용
  var price = document.getElementsByClassName("oldPrice");
  for (var i = 0; i < price.length; i++) {
    //   예전 가격을 가져와서
    var oldPrice = price[i].innerText;
    //  새로 할인 될 가격을 적용 20%
    var newPrice = oldPrice - oldPrice / 5;
    $(`#newPrice${price[i].id}`).text(newPrice);
  }

  // style
  var text = $(".style.WOMEN");
  for (var i = 0; i < text.length; i++) {
    var newText = text[i].innerText
      .replace("WOMEN", "여성")
      .replace("1 :", "")
      .replace("2 :", "")
      .replace("3 :", "")
      .replace("4 :", "")
      .replace("5 :", "");
    text[i].innerText = newText;
  }

  var text = $(".style.MEN");
  for (var i = 0; i < text.length; i++) {
    var newText = text[i].innerText
      .replace("MEN", "남성")
      .replace("1 :", "")
      .replace("2 :", "")
      .replace("3 :", "")
      .replace("4 :", "")
      .replace("5 :", "");
    text[i].innerText = newText;
  }
});
