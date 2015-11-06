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
    $('.selecter-options').mouseleave(function () {
        $(this).hide();
    });

    $('div').not('.selecter-item').on('mouseup', function () {
        $(options).hide();
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
    if (id == '') {
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
$("#category")
    .change(function () {
        var str = "";
        $("option:selected", this).each(function () {
            str += $(this).text() + " ";
        });
        $(".category-selected").text(str);
    })
    .trigger("change");
$("#state")
    .change(function () {
        var str = "";
        $("option:selected", this).each(function () {
            str += $(this).text() + " ";
        });
        $(".state-selected").text(str);
    })
    .trigger("change");

var indexOfImg = 0;
function setImgsToFile(){

    var $templateImg = $('#templateImg div').clone();
    var $childrenOfTmkImgs = $('#tmk-imgs').find('.tmk-img');


    var $lastOfTmkImgs = $childrenOfTmkImgs.last();
    if($childrenOfTmkImgs.length > 0 && $lastOfTmkImgs.find("img").attr('src') == "") $lastOfTmkImgs.remove();

    var $filePhoto = $templateImg.find('.filePhoto');

    if($childrenOfTmkImgs.length > 0) {
        $filePhoto.attr('id', 'filePhoto' + (parseInt($('#tmk-imgs').find('.filePhoto').last().attr('id').replace(/[^0-9\.]/g, ''),10) + 1));
    }

    $filePhoto.bind('change', handleImage);

    $('#tmk-imgs').append($templateImg);

    return $filePhoto;
}
function putImgsToFile() {
    var $filePhoto = setImgsToFile();
    $filePhoto.click();
}
//document.getElementById("input-image").innerHTML("<input type=\"file\"" + "name=\"image\"" + "id=\"" + 'filePhoto' + (indexOfImg + 1) + "\"/>");
//var imageLoader = document.getElementById('filePhoto' + (indexOfImg + 1));
//imageLoader.addEventListener('change', handleImage, false);

//var imageLoader = document.getElementById('filePhoto1');
//imageLoader.addEventListener('change', handleImage, false);


function handleImage(e) {
    var reader = new FileReader();
    reader.onload = function (event) {
        $(e.target).parent().find('img').attr('src', event.target.result);
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
    //this code line fires your 'handleImage' function (imageLoader change event)
    //var imageLoaderTarget = document.getElementById('filePhoto');
    //imageLoaderTarget.files = files;
    var $imageLoaderTarget = setImgsToFile();
    $imageLoaderTarget[0].files = files;
}

function deleteImg(span) {
    var $deleteImgWrap = $(span).parent();
    $deleteImgWrap.remove();

}
//
//function stepper(stepper) {
//    var $stepper = $(stepper);
//    var $input = $stepper.siblings('input');
//    var value = parseInt($input.val());
//    if ($stepper.text() == 'up') {
//        if (value < parseInt($input.attr('max'))) {
//            value = value + 1;
//            $input.val(value);
//        }
//    } else {
//        if (value > parseInt($input.attr('min'))) {
//            value = value - 1;
//            $input.val(value);
//        }
//    }
//}