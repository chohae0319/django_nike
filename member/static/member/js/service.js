$(document).ready(function() {
  function createIssue(issueTitle, issueBody) {
    var url = `https://api.github.com/repos/Minsoo-web/react-blog/issues`;
    $.ajax({
      url: url,
      type: "POST",
      headers: {
        Authorization: "token fb55268f6981e64c405d557c1e5d8f5d7563c872",
        "content-type": "application/json"
      },
      data: JSON.stringify({
        title: issueTitle,
        body: issueBody,
        labels: ["help wanted"]
      }),
      success: function() {
        console.log("성공");
      },
      error: function() {
        console.log("에러");
      }
    });
  }
  $("#get").click(function() {
    $.ajax({
      url: "https://api.github.com/repos/Minsoo-web/react-blog/issues",
      type: "GET",
      headers: {
        Authorization: "token fb55268f6981e64c405d557c1e5d8f5d7563c872",
        "content-type": "application/json"
      },
      datatype: "json",
      success: function(data) {
        console.log(data[0]);
        var issueNum = data[0].number;
        var issueTitle = data[0].title;
        var issueBody = data[0].body;
        $("#getTitle").text(issueTitle);
        $("#getBody").text(issueBody);
        $("#issueNum").text(issueNum);
      },
      error: function() {
        console.log("에러");
      }
    });
  });
  $("#submit").on("click", function() {
    var issueTitle = $("#title").val();
    var issueBody = $("#body").val();
    createIssue(issueTitle, issueBody);
  });
});
