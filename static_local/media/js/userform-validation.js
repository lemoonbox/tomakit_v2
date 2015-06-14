// <![CDATA[
jQuery( function ($) {
  var re_id_email = /^[0-9a-zA-Z]([\-.\w]*[0-9a-zA-Z\-_+])*@([0-9a-zA-Z][\-\w]*[0-9a-zA-Z]\.)+[a-zA-Z]{2,9}$/; //email
  var re_nick_name = /^[가-힣a-zA-Z]{2,15}$/; //아이디 검사식
//  var re_id_password, re_id_password_confirm = /(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{6,16}$/; //pw

  //                 var re_url = /^(https?:\/\)?([a-z\d\.-]+)\/([a-z\.]{2,6})([\/\w\.-]*)*\/?$/; //url
  //                 var re_tel = /^[0-9]{8,11}$/; //tel

  var
  form = $('.form-signin'),
      nick_name = $('#nick_name'),
      id_password = $('#id_password'),
      id_password_confirm = $('#id_password_confirm'),
      id_email = $('#id_email');
  //            url = $('#url'),
  //            tel = $('#tel');


//  form.submit(function () {
//    if (form.val() === "") {
//      alert('모든 항목을 정확히 기입해주세요.');
//      return false;
//    }
//    return true;
//    else if (re_id_email.test(id_email.val()) != true) {
//      alert('@ 올바른 형식의 이메일이 아닌 것 같아요.');
//      id_email.focus();
//      return false;
//    } else 
  
//  if(id_password.val().length < 6) {
//      alert('비밀번호는 6자리 이상 18자리 이하로 입력해주세요.');
//      id_password.focus();
//      return false;
//    }
//  });
//    else if(re_nick_name.test(nick_name.val()) != true) {
//      alert('닉네임이 올바르지 않습니다.');
//      nick_name.focus();
//      return false;
//    } else if(id_password.val() != id_password_confirm.val()) {
//      alert('비밀번호가 일치하지 않습니다.');
//      id_password_confirm.focus();
//      return false;
//    }
//  });

  $('#id_email, #nick_name, #id_password, #id_password_confirm').after('<span class="help-text"></span>');

  id_email.keyup(function () {
    var s = $(this).next('span');
    if (id_email.val().length === 0) {
      s.text('');
    } else if (re_id_email.test(id_email.val()) !== true) {
      s.text(' ex) tomakit@gmail.com');
    } else {
      s.text('');
    }
  });

  nick_name.keyup(function () {
    var s = $(this).next('span');
    if (nick_name.val().length === 0) {
      s.text('');
    } else if (nick_name.val().length ==1 ) {
      s.text('최소 2자 이상 입력해주세요.');
    } else if (nick_name.val().length > 15) {
      s.text('15자 이내로 입력해주세요.');
    } else if (re_nick_name.test(nick_name.val()) !== true) {
      s.text('한글 혹은 영어만 사용할 수 있습니다.');
    } else if (re_nick_name.test(nick_name.val()) === true) {
      s.text('');
    }
  });
    
  id_password.keyup(function () {
    var s = $(this).next('span');
    if (id_password.val().length === 0) {
      s.text('');
    } else if (id_password.val().length <= 6) {
      s.text(' 비밀번호를 6자리 이상 입력해주세요.');
    } else if (id_password.val().length >= 18) {
      s.text(' 18자리 이하로 입력해주세요.');
    } else {
      s.text(' 적당해요!');
    }
  });


  id_password_confirm.keyup(function () {
    var s = $(this).next('span');
    if (id_password_confirm.val() !== id_password.val()) {
      s.text(' 비밀번호가 일치하지 않습니다.');
    } else {
      s.text('');
    }
  });

  
  //          tel.keydown( function() {
  //            if(event.keyCode==109 || event.keyCode==189) {
  //               return false;
  //               }
  //               });
});
//]]> 