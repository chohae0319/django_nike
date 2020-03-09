$(document).ready(function() {
  $(".form-shipping-plus label").text("");
  $("#id_destination_nickname")
    .attr("placeholder", "배송지 이름")
    .before($("<span>배송지 이름</span>"));
  $("#id_receiver")
    .attr("placeholder", "이름")
    .before($("<span>받으시는 분</span>"));
  $("#id_receiver_phone")
    .attr("placeholder", "전화번호")
    .before($("<span>전화번호</span>"));
  $("#id_receiver_address")
    .attr("placeholder", "상세주소")
    .before($("<span>상세주소</span>"));
});
