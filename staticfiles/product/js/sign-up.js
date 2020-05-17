$(function () {
  // 클래스 추가
  $(".form-box-signUp input").addClass("sign-up-input");

  // 형식 맞춰주기 위한 label 텍스트 삭제
  $("label").text("");

  // placeholder 추가
  $("#id_email").attr(
    "placeholder",
    "사용하실 ID를 입력해주세요. (수신 가능 E-mail)"
  );
  // 포커스 주기
  $("#id_email").focus();

  // placeholder 추가
  // autofocus 속성 삭제
  $("#id_username")
    .attr("placeholder", "이름을 입력해주세요.")
    .removeAttr("autofocus");

  // placeholder 추가
  $("#id_password1").attr(
    "placeholder",
    "영문+숫자+특수문자 8~16자리(특수문자 괄호()는 사용 불가)"
  );
  $("#id_password2").attr("placeholder", "패스워드를 다시 입력해주세요.");
});

// sign-in
$(function() {
  // 클래스 추가
  $(".form-box-signIn input").addClass("sign-in-input");

  // placeholder 추가
  // autofocus 속성 삭제
  $(".form-box-signIn #id_username")
    .attr("placeholder", "이름")
    .removeAttr("autofocus");

  // placeholder 추가
  $("#id_password").attr("placeholder", "비밀번호");
});
