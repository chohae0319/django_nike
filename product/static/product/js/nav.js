$(function() {
  $("#search-icon").click(function() {
    $(".hide-search").toggleClass("none-hide");
  });
});

// 모바일 검색창에서 검색창 누를 시 모달 창 띄우기
$(function() {
  $("#hide-search-input").focus(function() {
    $("#hide-search-modal").toggleClass("big-modal");
  });
});

// 모달 띄울 시 스크롤 막기
$(function() {
  $("#hamburger label").click(function() {
    $("body").css("overflow", "hidden");
  });
  $("#whole-wrapper").click(function() {
    $("body").css("overflow", "auto");
  });
});

// 로그인 모달
$(document).ready(function() {
  //  키는 거
  $("#open-login").click(function() {
    $(".whole-wrapper-login").css({ display: "block" });
    $(".login-modal").css({ display: "block" });
    $("body").css({ overflow: "hidden" });
    $("#email-verify").css({ display: "block" });
    $("#email-verified").css({ display: "none" });
  });
  //  끄는거
  $("#close-login").click(function() {
    $(".whole-wrapper-login").css({ display: "none" });
    $(".login-modal").css({ display: "none" });
    $("body").css({ overflow: "auto" });
  });
  $(".whole-wrapper-login").click(function() {
    $(".whole-wrapper-login").css({ display: "none" });
    $(".login-modal").css({ display: "none" });
    $(".find-membership-modal").css({ opacity: "0", display: "none" });
    $("body").css({ overflow: "auto" });
  });

  //  아이디 찾기
  $("#find-membership-btn").click(function() {
    $(".find-membership-modal").css({ opacity: "1", display: "block" });
  });

  // 창 닫기
  $(".close-find-membership i").click(function() {
    $(".whole-wrapper-login").css({ display: "none" });
    $(".find-membership-modal").css({ opacity: "0", display: "none" });
    $(".login-modal").css({ display: "none" });
    $("body").css({ overflow: "auto" });
    $("#email-verify").css({ display: "block" });
    $("#email-verified").css({ display: "none" });
  });

  // 로그인으로 돌아가기
  $("#back-to-login").click(function() {
    $(".find-membership-modal").css({ opacity: "0", display: "none" });
    $("#email-verify").css({ display: "block" });
    $("#email-verified").css({ display: "none" });
  });

  // 다음단계 진행하기
  $("#submit-email").click(function() {
    var email = $("#input-email").val();
    var expert = /^[A-Za-z0-9\.\-]+@[A-Za-z0-9\-]+\.[A-Za-z0-9\-]+/;
    console.log(email.length);
    if (email.length === 0) {
      $("#email-alert-msg").text("이메일을 입력해주세요");
    } else if (expert.test(email) == false) {
      $("#email-alert-msg").text("이메일 형식에 맞게 입력해주세요");
      console.log("ASD");
    } else {
      $.ajax({
        type: "POST",
        url: "/member/id-find/",
        data: {
          email: email,
          csrfmiddlewaretoken:
            "SDMhjD8JzOKYVkPjrnx8diP4cLAjjmtcWEauEZHX7DQg8NDl2CkkaIzj3iyLjKn3"
        },
        success: function(response) {
          // 성공시 다음단계 진행
          $("#email-alert-msg").text("");
          $("#email-verify").css({ display: "none" });
          $("#email-verified").css({ display: "block" });
          console.log(response);
        },
        error: function() {
          console.log("에러");
        }
      });
    }
  });

  //  이전단계로 돌아가기
  $("#back-to-lastStep").click(function() {
    $("#email-verify").css({ display: "block" });
    $("#email-verified").css({ display: "none" });
  });
});

//  모바일 환경 nav 필터
$(document).ready(function() {
  // filter 버튼 클릭시
  $(`#mobile-toggle-aside`).click(function() {
    $("#aside-product").css({ display: "block" });
    $(".whole-wrapper-login").css({ display: "block" });
    $("body").css({ overflow: "hidden" });
  });
  // 검정 화면 클릭시
  $(".whole-wrapper-login").click(function() {
    $("#aside-product").css({ display: "none" });
    $(".whole-wrapper-login").css({ display: "none" });
    $("body").css({ overflow: "auto" });
  });
  //  사이즈 선택시
  $(".size-label").click(function() {
    var windowWidth = $(window).width();
    if (windowWidth > 883) {
      return;
    } else {
      $("#aside-product").css({ display: "none" });
      $(".whole-wrapper-login").css({ display: "none" });
      $("body").css({ overflow: "auto" });
    }
  });
  $(window).resize(function() {
    var windowWidth = $(window).width();
    if (windowWidth > 883) {
      $("#aside-product").css({ display: "block" });
    } else {
      $("#aside-product").css({ display: "none " });
    }
  });
});
