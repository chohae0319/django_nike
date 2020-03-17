$(function() {
  var rate = document.getElementById("user-rate").innerText;
  var maxPrice = document.getElementById("max-price");
  var currentPrice = Number(document.getElementById("current-price").innerText);

  switch (rate) {
    case "MVP":
      maxPrice.innerText = "1,000,000원";
      var max = 1000000;
      var percent = (currentPrice / max) * 100;
      $("#order-percent").text(`(${percent}%)`);
      $("div.percentage").css({ width: `100%` });
      $("span.percentage").css({ left: `99%` });
      break;

    case "PLATINUM":
      maxPrice.innerText = "1,000,000원";
      var max = 1000000;
      var percent = (currentPrice / max) * 100;
      $("#order-percent").text(`(${percent}%)`);
      $("div.percentage").css({ width: `${percent}%` });
      $("span.percentage").css({ left: `${percent - 1}%` });
      break;

    default:
      maxPrice.innerText = "500,000원";
      var max = 500000;
      var percent = (currentPrice / max) * 100;
      $("#order-percent").text(`(${percent}%)`);
      $("div.percentage").css({ width: `${percent}%` });
      $("span.percentage").css({ left: `${percent - 1}%` });
      break;
  }
});
