$(function() {
    $('.vote-form').ajaxForm(function () {
    });

    $('.vote-form select').bind('change', function (event) {
        $(this).closest('form').submit();
    });
//    $('button').click(function (event) {
//        event.preventDefault();
//        alert('hey');
//    })
})
