// ajax votes
$(function() {
    $('.vote-form').ajaxForm(function () {
    });

    $('.vote-form select').bind('change', function (event) {
        $(this).closest('form').submit();
    });
})

// load more contests
//
// display more contests
var appendContests = function(contests){
    $('.contests').find('tbody').append(contests);
}

var callBack = function(data, textStatus, jqXHR){
    appendContests(data);
}

$(function() {
    $('.show-more-contests').click(function (e){
        e.preventDefault();
        $.get('/contests', callBack);
    })
})
