var quantity = 1;
$(document).ready(function() {
  // 카운터
  $("#numOfItems").text(quantity);
  // +
  $("#increaseNum").click(function() {
    var checked = $(`input[name="inventory"]:checked`).val();
    if (checked === undefined) {
      $("#size-alert").text("사이즈를 골라주세요");
      return;
    } else {
      var span = Number($(`#size-${checked}`).text());
      if (quantity >= span) {
        $("#size-alert").text(`${span}개까지 구매 가능한 상품입니다.`);
        return;
      }
      $("#size-alert").text("");
      quantity = quantity + 1;
      $("#numOfItems").text(quantity);
    }
  });
  // -
  $("#decreaseNum").click(function() {
    var checked = $(`input[name="inventory"]:checked`).val();
    if (quantity === 0) {
      return;
    } else if (checked !== undefined) {
      $("#size-alert").text("");
    }
    quantity = quantity - 1;
    $("#numOfItems").text(quantity);
  });
});
