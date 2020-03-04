var userInfo = {
  name: "",
  phone: "",
  address: "",
  memo: ""
};
var nextStep = false;
$(function() {
  $(".input-info").on("blur", function() {
    // 미입력시
    if ($(this).val().length === 0) {
      $(this)
        .prev()
        .text("필수 입력란입니다.")
        .attr("style", "color :rgb(248, 84, 32)");
      // 공백으로 저장
      userInfo = {
        ...userInfo,
        [this.name]: this.value
      };
      // 콘솔창 확인용
      console.log(userInfo);
      return false;
    } else {
      // 제대로 입력했다면 경고 문구 삭제
      $(this)
        .prev()
        .text("")
        .attr("style", "color : black");
      // 값 저장
      userInfo = {
        ...userInfo,
        [this.name]: this.value
      };
      // 콘솔창 확인용
      console.log(userInfo);
    }
  });
});

$(function() {
  $("#checkout-next").click(function() {
    //   userInfo의 길이만큼 반복하며 입력 안 한게 있는지 검사
    for (var i = 0; i < Object.keys(userInfo).length; i++) {
      if (userInfo[Object.keys(userInfo)[i]] === "") {
        alert(Object.keys(userInfo)[i] + "을 입력해주세요");

        $(`input[name=${Object.keys(userInfo)[i]}]`).focus();
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
    for (var i = 0; i < Object.keys(userInfo).length; i++) {
      if (userInfo[Object.keys(userInfo)[i]] === "") {
        alert(Object.keys(userInfo)[i] + "을 입력해주세요");

        $(`input[name=${Object.keys(userInfo)[i]}]`).focus();
        return;
      }
    }

    // 터치 이벤트 활성화
    $(".checkout-next-step").removeClass("checkout-next-step");
    // 현재 단계 자동 접음
    $("#checkout-address-detail")
      .removeAttr("checked")
      .prop("checked", false);
    // input 창은 안 보이게 가려줌
    $(".input-info").attr("style", "display : none");
    // 정보 텍스트화
    $("#receive_name_info").text($("#receive_name").val());
    $("#receive_phone_info").text($("#receive_phone").val());
    $("#receive_address_info").text($("#receive_address").val());
    $("#receive_memo_info").text($("#memo").val());
    $("#after-address").text(userInfo.address);

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

// 배송지가 있을때 다음단계 진행
$(function() {
  $("#checkout-next2").click(function() {
    var alertMsg = $("#alert-msg-next");
    if ($(`input[name="address-tab"]:checked`).val() === "newAddress") {
      //   userInfo의 길이만큼 반복하며 입력 안 한게 있는지 검사
      for (var i = 0; i < Object.keys(userInfo).length; i++) {
        if (userInfo[Object.keys(userInfo)[i]] === "") {
          alertMsg.text(Object.keys(userInfo)[i] + "을 입력해주세요");

          $(`input[name=${Object.keys(userInfo)[i]}]`).focus();
          return;
        }
      }
    } else if ($(`input[name="address-tab"]:checked`).val() === "oldAddress") {
      var number = $(".selected-address").length;
      var memo = $("#checkout-address-memo").val();
      if (!memo) {
        alertMsg.text("배송 메모를 작성해주세요");
        return;
      }
      if (number === 0) {
        alertMsg.text("배송받으실 주소를 선택해주세요");
        return;
      } else if (number !== 1) {
        alertMsg.text("하나의 배송지만 선택해주세요");
        return;
      }
      // 다 만족했을 때
      else {
        alertMsg.text("");
        userInfo = {
          ...userInfo,
          memo: memo
        };
        nextStep = true;
        console.log(userInfo);
        console.log(nextStep);
      }
    }
    // 정보 텍스트화
    $("#checkout-username").text(userInfo.name);
    $("#checkout-address").text(userInfo.address);
    $("#checkout-phone").text(userInfo.phone);
    $("#checkout-memo").text(userInfo.memo);
    $("#after-address").text(userInfo.address);
    // 현재 단계 자동 접음
    $("#checkout-address-detail")
      .removeAttr("checked")
      .prop("checked", false);
    // 다음단계 활성화
    $("#checkout-pay-detail").prop("checked", true);
    $("#checkout-sale-detail").prop("checked", true);
    // 터치 이벤트 활성화
    $(".checkout-next-step").removeClass("checkout-next-step");
    // 다음단계 버튼 삭제
    $(this).css({ display: "none" });
    // 입력창 지움
    $("#input-user_address").css({ display: "none" });
    console.log(userInfo);
    return userInfo;
  });
});
$(document).ready(function() {
  $("#checkout-address-detail").click(function() {
    var number = $("#checkout-address-detail:checked").length;
    if (nextStep) {
      if (number === 1) {
        $("#before-next-step").css({ display: "block" });
      } else if (number !== 1) {
        $("#before-next-step").css({ display: "none" });
      }
    }
    // 다음단계가 아니라면
    else {
      return;
    }
  });
});

$(document).ready(function() {
  var oldtab = $("#checkout-address-tab-old");
  var newtab = $("#checkout-address-tab-new");
  var oldlabel = $("#checkout-address-label-old");
  var newlabel = $("#checkout-address-label-new");
  oldlabel.css({ backgroundColor: "white" });
  newlabel.css({ backgroundColor: "#e0e0e0" });

  // tab menu 클릭시 색상 변경
  $(`input[name="address-tab"]`).on("click", function() {
    var checkedRadio = $(`input[name="address-tab"]:checked`);
    if (checkedRadio.val() === "oldAddress") {
      oldlabel.css({ backgroundColor: "white" });
      newlabel.css({ backgroundColor: "#e0e0e0" });
    } else if (checkedRadio.val() === "newAddress") {
      newlabel.css({ backgroundColor: "white" });
      oldlabel.css({ backgroundColor: "#e0e0e0" });
    }
  });
  // 클릭한 주소 테두리
  // 클릭한 주소를 userInfo_old에 담는다.
  $(".checkout-address-oldList").on("click", function() {
    $(this).toggleClass("selected-address");
    var name = $(".selected-address .receiver-name").text();
    var address = $(".selected-address .receiver-address").text();
    var phone = $(".selected-address .receiver-phone").text();
    userInfo = {
      address: address,
      name: name,
      phone: phone,
      memo: ""
    };
    console.log(userInfo);
  });
});