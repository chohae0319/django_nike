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
  $("#open-login").click(function() {
    $(".whole-wrapper-login").css({ display: "block" });
    $(".login-modal").css({ display: "block" });
    $("body").css({ overflow: "hidden" });
  });
  $("#close-login").click(function() {
    $(".whole-wrapper-login").css({ display: "none" });
    $(".login-modal").css({ display: "none" });
    $("body").css({ overflow: "auto" });
  });
  $(".whole-wrapper-login").click(function() {
    $(".whole-wrapper-login").css({ display: "none" });
    $(".login-modal").css({ display: "none" });
    $("body").css({ overflow: "auto" });
  });
});
