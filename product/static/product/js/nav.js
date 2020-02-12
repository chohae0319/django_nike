// 검색 아이콘 클릭시 인풋창 띄우기
$(function() {
  $("#search-icon").click(function() {
    $(".hide-search").toggleClass("none-hide");
  });
});
//   인풋창 포커스시 모달창 띄우기
$(function() {
  $("#hide-search-input").focus(function() {
    $("#hide-search-modal").toggleClass("big-modal");
  });
});
