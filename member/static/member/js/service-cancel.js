$(document).ready(function() {
  var toggle = true;
  var product = [];
  var checkSelect = false;
  var inputTitle = "";
  var inputBody = "";
  var requestUser = "";

  function createIssue(inputTitle, inputBody, requestUser) {
    var url = `https://api.github.com/repos/Minsoo-web/react-blog/issues`;
    $.ajax({
      url: url,
      type: "POST",
      headers: {
        Authorization: "token e07ce42e16e8f0cf7f1f38f7d8c9a3656662e0bb",
        "content-type": "application/json"
      },
      data: JSON.stringify({
        title: inputTitle,
        body: inputBody,
        labels: ["help wanted", requestUser]
      }),
      success: function() {
        window.location.href = "/member/service-complete";
      },
      error: function() {
        window.location.href = "../../product/error";
      }
    });
  }

  $(".order-dropdown-wrapper>p").click(function() {
    $(".toggle-ul").toggleClass("show");
    $("#xi-icons").toggleClass("updown");
    var numOfItems = $(".order-list-wrapper").length;

    for (var i = 0; i < numOfItems; i++) {
      var productName = $(".product-name")[i].innerHTML;
      var productPrice = $(".product-price")[i].innerHTML;
      var productSize = $(".product-size")[i].innerHTML;
      var productQuantity = $(".product-quantity")[i].innerHTML;
      var productDate = $(".product-date")[i].innerHTML;
      var productImgUrl = $(".product-url")[i].innerHTML.replace(
        "product",
        "media/product"
      );
      var productStyle = $(".product-style")[i].innerHTML;
      var productOrderNum = $(".product-orderNum")[i].innerHTML;

      var productItem = {
        name: productName,
        price: productPrice,
        size: productSize,
        quantity: productQuantity,
        date: productDate,
        url: productImgUrl,
        style: productStyle,
        orderNum: productOrderNum,
        body: "",
        user: ""
      };
      if (toggle) {
        product.push(productItem);
      }
    }
    console.log(product);
    if (toggle) {
      for (var i = 0; i < numOfItems; i++) {
        $(".toggle-ul").append(
          `<li class="ordered-product-list list${i}">${product[i].name}</li>`
        );
      }
      toggle = false;
    }
    $(".ordered-product-list").click(function() {
      checkSelect = true;
      var classNum = Number(
        $(this)
          .attr("class")
          .replace("ordered-product-list", "")
          .replace("list", "")
      );
      $(".checked-product").text(product[classNum].name);
      $("#product-thumNail").attr("src", `../../${product[classNum].url}`);
      $("#checked-style").text(`스타일 : ${product[classNum].style}`);
      $("#checked-size").text(`사이즈 : ${product[classNum].size}`);
      $("#checked-quantity").text(`수량 : ${product[classNum].quantity}`);
      $("#checked-price").text(`결제 금액 : ${product[classNum].price}원`);

      // 제출하기
      $("#submit-btn").click(function() {
        if (checkSelect) {
          var title = $("#cancel-input-title").val().length;
          var body = $("#cancel-input-body").val().length;
          // 둘다 없을 때
          if (!title && !body) {
            $(".alert-msg-title").text("필수사항입니다.");
            $(".alert-msg").text("필수사항입니다.");
          }
          // 제목만 없을때
          else if (!title && body) {
            $(".alert-msg-title").text("필수사항입니다.");
            $(".alert-msg").text("");
          }
          // 바디만 없을때
          else if (title && !body) {
            $(".alert-msg-title").text("");
            $(".alert-msg").text("필수사항입니다.");
          }
          // 다 걸른 최종 상태
          else {
            $(".alert-msg-title").text("");
            $(".alert-msg").text("");
            console.log(product[classNum]);
            inputTitle = $("#cancel-input-title").val();
            product.body = $("#cancel-input-body").val();
            product.user = $("#userName").val();
            requestUser = product.user;
            inputBody = `- 취소 신청 제품 : ${product[classNum].name} <br/> - 주문번호 : ${product[classNum].orderNum}  <br/> - 수량 : ${product[classNum].quantity}  <br/> - 사이즈 : ${product[classNum].size}  <br/>  - 결제 금액  : ${product[classNum].price} <br/> - 취소 사유 :  ${product.body} <br/> - 결제한 시각 : ${product[classNum].date} `;
            // issue function
            createIssue(inputTitle, inputBody, requestUser);
          }
        }
      });
    });
  });

  //  안 골랐을 경우
  $("#submit-btn").click(function() {
    if (!checkSelect) {
      alert("상품을 골라주세요");
    }
  });
  // toggle 접기
  $(".toggle-ul").click(function() {
    $(this).toggleClass("show");
    $("#xi-icons").toggleClass("updown");
  });
});
