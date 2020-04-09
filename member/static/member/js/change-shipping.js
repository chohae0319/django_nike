$(document).ready(function() {
  $(`.shipping-info-wrapper label[for="order-shipping-modify"]`).click(
    function() {
      var classNum = $(this).attr("class");
      var num = Number(classNum.replace("change-shipping", ""));
      console.log(num);
      var arr = $(`.shipping-point-wrapper .${classNum}`);
      var array = [];
      array.push(arr);
      var address = array[0][0].textContent;
      var receiver = array[0][1].textContent;
      var phone = array[0][2].textContent;
      var memo = array[0][3].textContent;

      $("#modify-shipping-receiver").val(receiver);
      $("#modify-shipping-address").val(address);
      $("#modify-shipping-phone").val(phone);
      $("#modify-shipping-memo").val(memo);
      $("#modify-shipping-id").val(num);
      $("#order-shipping-modal form").attr(
        "action",
        `order-shipping-update/${num}`
      );
      $("#order-shipping-modal").css({ display: "block" });
      $(".order-shipping-box").css({ display: "block" });
      $("body").css({ overflow: "hidden" });
    }
  );
  $(`.order-shipping-box label[for="order-shipping-modify"]`).click(function() {
    $("#order-shipping-modal").css({ display: "none" });
    $(".order-shipping-box").css({ display: "none" });
    $("body").css({ overflow: "auto" });
  });
  $("#order-shipping-modal").click(function() {
    $(this).css({ display: "none" });
    $(".order-shipping-box").css({ display: "none" });
    $("body").css({ overflow: "auto" });
  });
});
