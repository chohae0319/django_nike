$(function() {
  $("#search-icon").click(function() {
    $(".hide-search").toggleClass("none-hide");
  });
});

$(function() {
  $("#hide-search-input").focus(function() {
    $("#hide-search-modal").toggleClass("big-modal");
  });
});

$(function() {
  $(".search").focus(function() {
    $(".whole-wrapper").addClass("bg-black");
  });
  $(".search").blur(function() {
    $(".whole-wrapper").removeClass("bg-black");
  });
});
