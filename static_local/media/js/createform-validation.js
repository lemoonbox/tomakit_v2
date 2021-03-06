// <![CDATA[
jQuery(function ($) {
//  var re_id_title =
//  var re_id_email = /^[A-Za-z0-9_]+[A-Za-z0-9_.]*[@]{1}[A-Za-z0-9_]+[A-Za-z0-9_.]*[.]{1}[A-Za-z]{2,5}$/; //email
//  var re_nick_name = /^[가-힣a-zA-Z]{2,10}$/; //아이디 검사식
//  var re_id_password, re_id_password_confirm = /(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{6,16}$/; //pw

  //                 var re_url = /^(https?:\/\)?([a-z\d\.-]+)\/([a-z\.]{2,6})([\/\w\.-]*)*\/?$/; //url
  var re_id_contact_tel = /^[0-9]{8,11}$/; //tel
  var re_id_price, id_minimum, id_maximum = /^[0-9]{8,11}$/;

  
  var form = $('.create'),
      nick_name = $('#nick_name'),
      id_password = $('#id_password'),
      id_password_confirm = $('#id_password_confirm'),
      id_email = $('#id_email');
  //  url = $('#url'),
      id_contact_tel = $('#id_contact_tel');


  form.submit(function () {
    if (form.val() !== true) {
      alert('모든 항목을 정확히 기입해주세요.');
      return false;
    }
  });

  $('.create').after('<span class="help-text"></span>');

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
    if (nick_name.val().length > 10) {
      s.text('10자 이내로 입력해주세요.');
    } else if (nick_name.val().length < 2) {
      s.text('최소 2자 이상 입력해주세요.');
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

  id_contact_tel.keydown(function () {
    if (event.keyCode === 109 || event.keyCode === 189) {
      return false;
    }
  });
});


function jsOnlyNumber(varTextObj) {
var varLength = varTextObj.value.length;
  var varText = "";
  for (var inx = 0; inx < varLength; inx++) {
    if (jsCheckNumber(varTextObj.value.substring(inx, inx+1)) ) {
      varText = varText + varTextObj.value.substring(inx,inx+1);
    }
  }

//]]>  
