$(document).ready(function() {
  // 클래스 추가
  $(".form-box-signUp input").addClass("sign-up-input");

  // 형식 맞춰주기 위한 label 텍스트 삭제
  $(".form-box-signUp p label").text("");

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
$(document).ready(function() {
  // 클래스 추가
  $(".form-box-signIn input").addClass("sign-in-input");
  $(".form-box-signIn p label").text("");
  // placeholder 추가
  // autofocus 속성 삭제
  $(".form-box-signIn #id_username")
    .attr("placeholder", "이름")
    .removeAttr("autofocus");

  // placeholder 추가
  $("#id_password").attr("placeholder", "비밀번호");
});

// member - update
$(document).ready(function() {
  $(
    "#profile-update #id_user_permissions,#id_is_staff,#id_is_active,#id_date_joined"
  ).remove();

  $("#profile-update .helptext").remove();
  $("#profile-update label").remove();
  $("#profile-update #id_password").remove();
  $("#profile-update #id_is_superuser").remove();
  $("#profile-update #id_groups").remove();

  $("#id_username").focus();

  $("#profile-update #id_first_name").attr("placeholder", "firstname");
  $("#profile-update #id_last_name").attr("placeholder", "lastname");
  $("#profile-update br").remove();
  $("#profile-update #id_last_login").remove();
  $("#profile-update #id_first_name,#id_last_name").after($("<br/><br/><br/>"));

  $("#profile-update #id_email").after($("<br/><br/><br/>"));
  $("#profile-update #id_username").after($("<br/><br/><br/>"));

  $("#profile-update #id_username").before($("<div>아이디</div>"));
  $("#profile-update #id_first_name").before($("<div>이름</div>"));
  $("#profile-update #id_last_name").before($("<div>성</div>"));
  $("#profile-update #id_email").before($("<div>이메일</div>"));
  $("#profile-update :focus").blur();
});

// 비밀번호 변경
$(document).ready(function() {
  $("#profile-password ul").remove();
  $("#profile-password label").remove();
  $(
    "#profile-password #id_old_password,#id_new_password1,#id_new_password2"
  ).after($("<br/><br/><br/>"));
  $("#profile-password #id_old_password").before($("<div>기존 비밀번호</div>"));
  $("#profile-password #id_new_password1").before(
    $("<div>새 비밀번호 입력</div>")
  );
  $("#profile-password #id_new_password2").before(
    $("<div>새 비밀번호 확인</div>")
  );
  $("#profile-password #id_email").before($("<div>이메일</div>"));
});
