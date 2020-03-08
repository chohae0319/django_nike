$(document).ready(function() {
  //  수정하기 버튼 클릭 시
  $(`label[val="open-update-shipping"]`).click(function() {
    $("#modify-form").css({ display: "block" });
    $("#remove-form").css({ display: "none" });
    // 수정 누른 label의 클래스 값을 가져와서
    var shippingNum = $(this).attr("class");
    //  같은 클래스 명의 input을 찾고
    var array = [];
    var arr = $(`span.${shippingNum}`);
    array.push(arr);
    console.log(shippingNum);
    console.log(array[0][0]);
    var nickname = array[0][0].textContent;
    var receiver = array[0][1].textContent;
    var address = array[0][2].textContent;
    var phone = array[0][3].textContent;

    $("#modify-shipping-nickName").val(nickname);
    $("#modify-shipping-receiver").val(receiver);
    $("#modify-shipping-phone").val(phone);
    $("#modify-shipping-address").val(address);
    $(".shipping-box>div#modify-form>form").attr(
      "action",
      `/order/shipping-update/${shippingNum}`
    );
    //  수정 부분 띄워주고
    //   삭제 부분은 가려주기
  });
  $(`label[val="open-remove-shipping"]`).click(function() {
    $("#remove-form").css({ display: "block" });
    $("#modify-form").css({ display: "none" });
    var shippingNum = $(this).attr("class");
    $(".shipping-box>div#remove-form>form").attr(
      "action",
      `/order/shipping-delete/${shippingNum}`
    );
  });
});
