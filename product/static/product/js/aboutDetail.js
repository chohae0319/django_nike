$(function () {
  const category2 = $("#category2").text();
  const category3 = $("#category3").text();

  $("#aboutDetail").css({
    background: `url("/static/product/img/${category2}-${category3}.png") no-repeat
  center/100% `,
  });
});
