var userinfo = {
  이름: "",
  연락처: "",
  주소: "",
  메모: ""
};

$(function() {
  $(".input-info").on("blur", function() {
    // 미입력시
    if ($(this).val().length === 0) {
      $(this)
        .prev()
        .text("필수 입력란입니다.")
        .attr("style", "color :rgb(248, 84, 32)");
      // 공백으로 저장
      userinfo = {
        ...userinfo,
        [this.name]: this.value
      };
      // 콘솔창 확인용
      console.log(userinfo);
      return false;
    } else {
      // 제대로 입력했다면 경고 문구 삭제
      $(this)
        .prev()
        .text("")
        .attr("style", "color : black");
      // 값 저장
      userinfo = {
        ...userinfo,
        [this.name]: this.value
      };
      // 콘솔창 확인용
      console.log(userinfo);
    }
  });
});

$(function() {
  $("#checkout-next").click(function() {
    //   userinfo의 길이만큼 반복하며 입력 안 한게 있는지 검사
    for (var i = 0; i < Object.keys(userinfo).length; i++) {
      if (userinfo[Object.keys(userinfo)[i]] === "") {
        alert(Object.keys(userinfo)[i] + "을 입력해주세요");

        $(`input[name=${Object.keys(userinfo)[i]}]`).focus();
        return;
      }
    }
    // 현재 단계 자동 접음
    $("#checkout-address-detail").removeAttr("checked");
    // input 창은 안 보이게 가려줌
    $(".input-info").attr("style", "display : none");

    // 다음단계 활성화
    $("#checkout-pay-detail").prop("checked", true);
    $("#checkout-sale-detail").prop("checked", true);
    // 터치 이벤트 활성화
    $(".checkout-next-step").removeClass("checkout-next-step");

    // 정보 텍스트화
    $("#receive_name_info").text($("#receive_name").val());
    $("#receive_phone_info").text($("#receive_phone").val());
    $("#receive_address_info").text($("#receive_address").val());
    $("#receive_memo_info").text($("#memo").val());
    // 다음단계 진행 버튼 비활성화 및 수정 버튼 활성화
    $("#checkout-next").attr("style", "display : none");
    $(this)
      .next()
      .attr("style", "display : block");
  });
  //   수정하기 버튼
  $("#modify-client-detail").click(function() {
    $(".input-info").attr("style", "display : block");
    $("#modify-client").attr("style", "display : block");
    $(this).attr("style", "display : none");
    // 다음단계 활성화
    $("#checkout-pay-detail").prop("checked", false);
    $("#checkout-sale-detail").prop("checked", false);
    // 터치 이벤트 활성화
    $("#checkout-address-box ~ .checkout-tab-box").addClass(
      "checkout-next-step"
    );
  });
  $("#modify-client").click(function() {
    for (var i = 0; i < Object.keys(userinfo).length; i++) {
      if (userinfo[Object.keys(userinfo)[i]] === "") {
        alert(Object.keys(userinfo)[i] + "을 입력해주세요");

        $(`input[name=${Object.keys(userinfo)[i]}]`).focus();
        return;
      }
    }

    // 터치 이벤트 활성화
    $(".checkout-next-step").removeClass("checkout-next-step");
    // 현재 단계 자동 접음
    $("#checkout-address-detail").removeAttr("checked");
    // input 창은 안 보이게 가려줌
    $(".input-info").attr("style", "display : none");
    // 정보 텍스트화
    $("#receive_name_info").text($("#receive_name").val());
    $("#receive_phone_info").text($("#receive_phone").val());
    $("#receive_address_info").text($("#receive_address").val());
    $("#receive_memo_info").text($("#memo").val());

    // 버튼 토글
    $(this).attr("style", "display : none");
    $(this)
      .prev()
      .attr("style", "display : block");
    // 다음단계 활성화
    $("#checkout-address-detail").prop("checked", false);
    $("#checkout-pay-detail").prop("checked", true);
    $("#checkout-sale-detail").prop("checked", true);
  });
});
