$(document).ready(function() {

    $('a.like').click(function (e) {
        console.log("new like btn clicked");
        e.preventDefault();
        var likeUrl = $(this).attr('href');
        console.log(likeUrl);
        console.log($(this).data('action'));
        $.post(
            likeUrl,
            {
                action: $(this).data('action')
            },
            function (data) {
                console.log(data['status']);
                console.log(data);
                if(data['status'] === 'ok') {
                    var previous_action = $('a.like').data('action');
                    console.log("previous action", previous_action);

                    // toggle data-action
                    $('a.like').data('action', previous_action === 'like' ? 'Unlike' : 'like');
                    // toggle link text
                    $('a.like').text(previous_action === 'like' ? 'Unlike' : 'like');

                    // update total likes
                    var previous_likes = parseInt($('#likeCount').text());
                    console.log("previous likes", previous_likes);
                    console.log("likeCount", $('#likeCount').text);
                    console.log("likeCount", $('#likeCount').innerText);
                    $('#likeCount').text(previous_action === 'like' ? previous_likes + 1 : previous_likes - 1);
                }
            }
        );
    });


    /*********************************      OR    ********************************************/

    /*function updateText(btn, newCount, verb) {
        btn.text(newCount + " " + verb);
        btn.attr("data-likes", newCount);
    }

    $(".like-btn").click(function (e) {
        console.log("like btn clicked");
        e.preventDefault();
        var this_ = $(this);
        var likeUrl = this_.attr('data-href');
        var likeCount = parseInt(this_.attr('data-likes')) | 0;
        var addLike = likeCount + 1;
        var removeLike = likeCount - 1;
        if (likeUrl) {
            $.ajax({
                url: likeUrl,
                method: "GET",
                data: {},
                success: function (data) {
                    console.log(data);
                    var newLikes;
                        if (data.liked) {
                            //add one like
                            updateText(this_, addLike, "Unlike")
                        } else {
                            //remove one like
                            updateText(this_, removeLike, "Like")
                        }
                }, error:
                    function (error) {
                        console.log(error)
                        console.log('error')
                    }
            })
        }
    })*/
});