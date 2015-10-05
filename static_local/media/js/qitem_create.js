/**
 * Created by jaewon on 15. 8. 1..
 */
function btnClick(selecterSelected) {
    var $select = $(selecterSelected).parent();
    var options = $select.find('.selecter-options').show();
    $('.selecter').css("z-index", "0");
    /**
     *     Mina added 4 lines below on 15.9.22
     */
    $select.css("z-index", "150");
    $('.selecter-options').mouseleave(function() {
        $(this).hide();
    });
}


function selecting(option, id) {
    var $selecterOptions = $(option).parent();

    var motionType = $selecterOptions.attr('data-value');
    var $selecter = $selecterOptions.parent();
    $selecter.find('.selecter-selected').html($(option).html());
    $selecterOptions.hide();
    $selecter.find('.selecter-item').removeClass("selected");
    $(option).addClass("selected");
    var formGroup = $selecterOptions.closest(".wgt-form-group");
    var $selecterHiddenInput = $(formGroup).nextAll().find('input[type=hidden]').eq(0);
    if(id == ''){
        id = $(option).attr('data-value');
        motionType = "00";
        $(formGroup).nextAll('.wgt-selecter').remove();
        $selecterHiddenInput.attr('data-value', "1");
    }

    $selecterHiddenInput.val(id);
    $selecter.find('select').val(id);


    $selecterOptions.hide();
    $selecterOptions.parent().css("z-index", "0");
}
$( "#category" )
    .change(function() {
        var str = "";
        $( "option:selected", this ).each(function() {
            str += $( this ).text() + " ";
        });
        $( ".category-selected").text( str );
    })
    .trigger( "change" );
$( "#state" )
    .change(function() {
        var str = "";
        $( "option:selected", this ).each(function() {
            str += $( this ).text() + " ";
        });
        $( ".state-selected").text( str );
    })
    .trigger( "change" );

var indexOfImg = 0;
function findLastInput(isOnclick){
    var $imgs = $('#tmk-imgs img');
    for(var i = 0; i < $imgs.length; i++){
        var $img = $imgs.eq(i);
        if($img.attr('src') == '') break;
    }
    indexOfImg = i;
    if(isOnclick) $('#filePhoto'+ (indexOfImg + 1)).click();
}

var imageLoader1 = document.getElementById('filePhoto1');
imageLoader1.addEventListener('change', handleImage, false);
var imageLoader2 = document.getElementById('filePhoto2');
imageLoader2.addEventListener('change', handleImage, false);
var imageLoader3 = document.getElementById('filePhoto3');
imageLoader3.addEventListener('change', handleImage, false);
var imageLoader4 = document.getElementById('filePhoto4');
imageLoader4.addEventListener('change', handleImage, false);
var imageLoader5 = document.getElementById('filePhoto5');
imageLoader5.addEventListener('change', handleImage, false);

function handleImage(e) {
    var reader = new FileReader();
    reader.onload = function (event) {
        $('#tmk-imgs img').eq(indexOfImg).attr('src',event.target.result);
    };
    reader.readAsDataURL(e.target.files[0]);
}

var dropbox;
dropbox = document.getElementById("filedrag");
dropbox.addEventListener("dragenter", dragenter, false);
dropbox.addEventListener("dragover", dragover, false);
dropbox.addEventListener("drop", drop, false);

function dragenter(e) {
    e.stopPropagation();
    e.preventDefault();
}

function dragover(e) {
    e.stopPropagation();
    e.preventDefault();
}

function drop(e) {
    e.stopPropagation();
    e.preventDefault();
    //you can check e's properties
    //console.log(e);
    var dt = e.dataTransfer;
    var files = dt.files;
    findLastInput();
    //this code line fires your 'handleImage' function (imageLoader change event)
    var imageLoaderTarget = document.getElementById('filePhoto'+(indexOfImg + 1));
    imageLoaderTarget.files = files;
}

function deleteImg(span){
    var $deleteImgWrap = $(span).parent();
    $deleteImgWrap.find('img').attr('src','');
    var $imgsWrap = $deleteImgWrap.parent();
    $imgsWrap.append($deleteImgWrap.detach());

}

function stepper(stepper) {
    var $stepper = $(stepper);
    var $input = $stepper.siblings('input');
    var value = parseInt($input.val());
    if ($stepper.text() == 'up') {
        if (value < parseInt($input.attr('max'))) {
            value = value + 1;
            $input.val(value);
        }
    } else {
        if (value > parseInt($input.attr('min'))) {
            value = value - 1;
            $input.val(value);
        }
    }
}