$(document).ready(function () {
  //  로딩과 동시에
  $.ajax({
    url: "https://api.github.com/repos/Minsoo-web/react-blog/issues",
    type: "GET",
    headers: {
      Authorization: "token 68a2056e6305014f4973d6dec375a3252b29f5a7",
      "content-type": "application/json",
    },
    datatype: "json",
    //  성공시
    success: function (data) {
      //   로그인 한 회원 것만 보이게
      console.log(data);
      var username = $("#username").text();
      var myList = data.filter(function (list) {
        if (list.labels[1].name) {
          return list.labels[1].name == username;
        }
      });
      console.log(myList);
      if (myList.length) {
        for (var i = 0; i < myList.length; i++) {
          //   월 일 까지만 보이게 자르기
          var date = myList[i].created_at.substring(0, 10);
          var title = myList[i].body.split("<br/>")[0].split(":");
          $(".cancel-list-wrapper").append(
            `<li class="cancel-list"><span>${myList[i].number}</span><span>${myList[i].title}</span><span>${myList[i].labels[1].name}</span><span>${date}</span><span>${title[1]}</span></li>`
          );
        }
      } else {
        $(".cancel-list-wrapper").append(
          "<li id='no-items'>현재 처리중인 상품이 없습니다.</li>"
        );
      }
    },
    error: function () {
      window.location.href = "../../product/error";
    },
  });
});
