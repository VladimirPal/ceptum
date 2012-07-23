$(document).ready(function() {
    $('a#next1').click(function() {
        $('.first-step').hide();
        $('.second-step').show();
    });

    $('a#next2').click(function() {
        $('.second-step').hide();
        console.log($('#browser'));
        $('.third-step').show();
    });

    $('a#add').click(function() {
        var newcam = $('.ip-cheap:first').clone();
        newcam.insertBefore($('.third-step a#add'))
    });

});
