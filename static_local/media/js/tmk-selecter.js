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

    $('div').not('.selecter-item').on('mouseup', function(){
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