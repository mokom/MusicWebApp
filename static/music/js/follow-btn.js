$(document).ready(function() {

    $('a.follow').click(function (e) {
        console.log("new follow btn clicked");
        e.preventDefault();
        var followUrl = $(this).attr('href');
        var d_action = $(this).attr('data-action');
        console.log(followUrl);
        console.log(d_action);
        $.post(
            followUrl,
            {
                action: $(this).data('action')
            },
            function (data) {
                console.log(data['status']);
                if(data['status'] == 'ok') {
                    var previous_action = $('a.follow').data('action');
                    console.log("previous action", previous_action);

                    // toggle data-action
                    $('a.follow').data('action', previous_action === 'follow' ? 'Unfollow' : 'follow');
                    // toggle link text
                    $('a.follow').text(previous_action === 'follow' ? 'Unfollow' : 'follow');

                    // update total likes
                    var previous_followers = parseInt($('#followerCount').text());
                    console.log("previous likes", previous_followers);
                    console.log("followerCount", $('#followerCount').text);
                    console.log("followerCount", $('#followerCount').innerText);
                    $('#followerCount').text(previous_action === 'follow' ? previous_followers + 1 : previous_followers - 1);
                }
            }
        );
    });

});