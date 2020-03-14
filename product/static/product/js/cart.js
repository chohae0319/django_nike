$(document).ready(function() {
  var toggle = true;
  $(".cart-item-option span").click(function() {
    var classNum = $(this).attr("value");
    var oldSize = $(`span.${classNum}`).text();
    $(".whole-wrapper-login").css({ display: "block" });
    $(".cart-option-modal").css({ display: "block" });
    $("body").css({ overflow: "hidden" });
    var pk = $(this).attr("class");
    $.ajax({
      type: "GET",
      url: "/cart/get-option/" + pk + "/",
      dataType: "json",
      success: function(response) {
        var answer = response.result;
        if (answer == "success") {
          if (toggle) {
            var category = response.option.category;
            var price = response.option.price;
            var name = response.option.name;
            if (category == "WOMEN 농구") {
              category = "WOMEN 골프";
            }
            $(".cart-product-category").text(category);
            $(".cart-product-price").text(`${price}원`);
            $(".cart-product-info-header h2").text(name);
            // 썸네일 추가
            $("#thumNail img").attr("src", `${response.option.image[0]}`);
            var numOfImg = response.option.image.length;
            //   사진 추가
            for (var i = 1; i < numOfImg; i++) {
              $("#thumNail").after(
                `<div class='cart-product-img-wrapper'><img src='${response.option.image[i]}' alt='제품상세이미지${i}'/></div>`
              );
            }
            //   label 추가
            //   사이즈 개수
            var inventoryNum = response.option.inventory.length;
            for (var i = 0; i < inventoryNum; i++) {
              // 해당 사이즈의 수량이 있으면
              if (response.option.inventory[i].amount) {
                if (response.option.inventory[i].size === oldSize) {
                  $(".size-selector").append(
                    `<input type='radio' checked name='inventory'  id='size${i}' value='${response.option.inventory[i].size}' /><label for='size${i}'>${response.option.inventory[i].size}</label><span>${response.option.inventory[i].amount}</span>`
                  );
                } else {
                  $(".size-selector").append(
                    `<input type='radio' name='inventory'  id='size${i}' value='${response.option.inventory[i].size}' /><label for='size${i}'>${response.option.inventory[i].size}</label><span>${response.option.inventory[i].amount}</span>`
                  );
                }
              } else {
                // 없으면 label에 class 추가
                $(".size-selector").append(
                  `<input type='radio' name='inventory'  id='size${i}' /><label class='no-amount' for='size${i}'>${response.option.inventory[i].size}</label><span>${response.option.inventory[i].amount}</span>`
                );
              }
            }
            console.log(response.option);
            //   옵션 변경 버튼
            //  여가에 ajax POST 넣으시면 됩니다.
            $(".cart-btn-wrapper span").click(function() {
              var checked = $(`input[name="inventory"]:checked`).val();
              console.log(checked);
            });
          }
        }
      }
    });
  });

  //   모달창 닫기 js
  $(".close-modal .xi-close").click(function() {
    $(".whole-wrapper-login").css({ display: "none" });
    $(".cart-option-modal").slideToggle(500);
    $("body").css({ overflow: "auto" });
    toggle = false;
  });
  $(".whole-wrapper-login").click(function() {
    $(".whole-wrapper-login").css({ display: "none" });
    $(".cart-option-modal").slideToggle(500);
    $("body").css({ overflow: "auto" });
    toggle = false;
  });
});
