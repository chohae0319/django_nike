var open = true;
$(document).ready(function() {
  var wrapper = $("#size-wrapper");
  $("#toggle-size").click(function() {
    var height = wrapper.height();
    //   열려있다면 접기
    if (open) {
      wrapper.css({ transform: `translateY(-${height + 55}px)` });
      open = false;
      return open;
    }
    // 접혀있다면 열기
    else {
      wrapper.css({ transform: "translateY(0)" });
      open = true;
      return open;
    }
  });

  // 사이즈 클릭시 검정 테두리
  $(".size-label").click(function() {
    $(this).toggleClass("black-label");
  });
});

// 체크된 사이즈 갯수 적어주기
$(document).ready(function() {
  $('input[name="size"]').on("click", function() {
    var size_checked_list = [];
    $('input[name="size"]:checked').each(function() {
      size_checked_list.push($(this).val());
    });
    if (size_checked_list.length === 0) {
      $("#aside-checked-size").text("");
    } else {
      $("#aside-checked-size").text(`(${size_checked_list.length})`);
    }
  });
});

// 필터 버튼 드롭다운
$(document).ready(function() {
  var filter = $("#filter-wrapper");
  var span = $("#filter-wrapper span");
  $("#filter-btn").click(function() {
    filter.addClass("filter-wrapper");
  });
  filter.on("mouseleave", function() {
    $(this).removeClass("filter-wrapper");
  });
  span.click(function() {
    var text = $(this).text();
    $("#current-filter").text(text);
  });
});
