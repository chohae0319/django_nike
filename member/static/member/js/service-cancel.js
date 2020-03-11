$(document).ready(function() {
  $(".order-dropdown-wrapper>p").click(function() {
    var numOfItems = $(".order-list-wrapper").length;

    var product = [];
    for (var i = 0; i < numOfItems; i++) {
      var productName = $(".product-name")[i].innerHTML;
      var productPrice = $(".product-price")[i].innerHTML;
      var productItem = {
        name: productName,
        price: productPrice
      };
      product.push(productItem);
    }
    console.log(product);
    for (var i = 0; i < numOfItems; i++) {
      $(".toggle-ul").append("<li></li>");
    }
  });
});
