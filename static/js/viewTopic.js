$('form.newcommentform').submit(function(e){
        e.preventDefault();
        var str = $(this).find('.mention').val();
        var pattern = /\B@[a-z0-9_.-]+/gi;
        var mentioned_users = str.match(pattern);
        $('<input>', {
          type: 'hidden',
          id: 'mentioned_user',
          name: 'mentioned_user',
          value: mentioned_users
        }).appendTo('form.editcommentform');

        var id = $(this).parent().prev().find('div.name').attr('id');
        var form = $(this);
        var formData = new FormData($(this)[0]);
        $.post('{% url "new_comment" %}', $(this).serialize(), function(data){
          if(data.error){
            console.log(data.response)

            $('div.error').remove();
            for (var key in data.response) {
              console.log(key)
              $('.newcommentform #' + key).after('<div class="error">' + data.response[key] + '</div>');
            }
          }
          else{
            window.location = ".";
          }
        }, 'json');
      });
      $('form.editcommentform').submit(function(e){
        e.preventDefault();
        console.log($(this).serialize())
        var str = $(this).find('.mention').val();
        var pattern = /\B@[a-z0-9_.-]+/gi;
        var mentioned_users = str.match(pattern);
        $('<input>', {
          type: 'hidden',
          id: 'mentioned_user',
          name: 'mentioned_user',
          value: mentioned_users
        }).appendTo('form.editcommentform');

        var id = $(this).parent().prev().find('div.name').attr('id');
        var form = $(this);
        var formData = new FormData($(this)[0]);
        $.post('{% url "new_comment" %}', $(this).serialize(), function(data){
          if(data.error){
            console.log(data.response)

            $('div.error').remove();
            for (var key in data.response) {
              console.log(key)
              $('.newcommentform #' + key).after('<div class="error">' + data.response[key] + '</div>');
            }
          }
          else{
            window.location = ".";
          }
        }, 'json');
      });
    $('form.edit_comment_form').submit(function(e){
        e.preventDefault();
        console.log($(this).serialize())
        var str = $(this).find('.mention').val();
        var pattern = /\B@[a-z0-9_.-]+/gi;
        var mentioned_users = str.match(pattern);
        $('<input>', {
          type: 'hidden',
          id: 'mentioned_user',
          name: 'mentioned_user',
          value: mentioned_users
        }).appendTo('form.edit_comment_form');
        url = $(this).attr('data-href')
        var id = $(this).parent().prev().find('div.name').attr('id');
        var form = $(this);
        var formData = new FormData($(this)[0]);
        $.post(url, $(this).serialize(), function(data){
          if(data.error){
            console.log(data.response)

            $('div.error').remove();
            for (var key in data.response) {
              console.log(key)
              $('.edit_comment_form #' + key).after('<div class="error">' + data.response[key] + '</div>');
            }
          }
          else{
            window.location = ".";
          }
        }, 'json');
      });
      $('.follow_topic').click(function(e){
        e.preventDefault();
        href = $(this).attr('data-href')
        $.post(href, {'topic_id': $(this).attr('id')}, function(data){
          if (data.is_followed){
            alert("You have succesfully followed the topic and will recieve the topic notifications !!!")
            $('.follow_topic').text('Followed')
          }
          else{
            $('.follow_topic').text('Follow')
          }
        });
      });

  function comment_users() {
    $.get("{% url 'get_mentioned_user' topic_id=topic.id %}", function(response){
        var users = response.data
        //comment_mentioned_user(users)
        $('.mention').suggest('@', {
          data: users,
          map: function(user) {
            return {
              value: user.username,
              text: '<strong>'+user.username+'</strong> <small>'+user.fullname+'</small>'
            }
          }
        })
      }
    )
  };

  comment_users();
function auto_link(link_id){
  $(link_id).each(function(){
    $(this).html( $(this).html().replace(/(@[\w?=&.\/-;#~%-]+(?![\w\s?&.\/;#~%"=-]*>))/gi, '<a href="$1">$1</a> ') );
    $(this).children().each(function(){
      var user_name = $(this).attr('href').replace(/\@/g,"");
      var url = "{% url 'show_player' }".replace(/1234/, user_name)
      $(this).attr('href', url);
    });
  });
}
$(document).ready(function(e){
  auto_link('.auto_link');
});
$('.delete-comment').click(function(e){
  e.preventDefault();
  href = $(this).attr('data-href');
  id = $(this).attr('id');
  $.post(href, $("form#jobform").serialize(), function(data) {
    if (!confirm('Do you want to delete Your Comment?'))
      return;
    if (data.error) {
      alert(data.response);
    } else {
      alert("Your Comment Deleted Successfully")
      $('#'+id).parent().parent().parent().remove();
    }
  }, 'json');
});

/* votes up and down */
{% if request.user.is_authenticated %}
  $("#down_vote").click(function(e){
    e.preventDefault();
    url = $(this).attr("data-href");
    $down_votes = $("#down_votes")
    $up_votes = $("#up_votes")
    $.get(url, function(response){
      if(response.status == "down"){
        count = parseInt($down_votes.text())
        $down_votes.text(count + 1);
      }
      else if(response.status == "removed"){
        count = parseInt($up_votes.text())
        $up_votes.text(count - 1);
      }
    });
  });
  $("#up_vote").click(function(e){
    e.preventDefault();
    url = $(this).attr("data-href");
    $down_votes = $("#down_votes")
    $up_votes = $("#up_votes")
    $.get(url, function(response){
      if(response.status == "up"){
        count = parseInt($up_votes.text())
        $up_votes.text(count + 1);
      }
      else if(response.status == "removed"){
        count = parseInt($down_votes.text())
        $down_votes.text(count - 1);
      }
    });
  });
  /* comment votes */
  $(".comment_down_vote").click(function(e){
    e.preventDefault();
    url = $(this).attr("data-href");
    $down_votes = $(this).parent().find("span.comment_down_votes_count")
    $up_votes = $(this).parent().find("span.comment_up_votes_count")
    console.log($down_votes.text())
    console.log($up_votes.text())
    $.get(url, function(response){
      if(response.status == "down"){
        count = parseInt($down_votes.text())
        $down_votes.text(count + 1);
      }
      else if(response.status == "removed"){
        count = parseInt($up_votes.text())
        $up_votes.text(count - 1);
      }
    });
  });
  $(".comment_up_vote").click(function(e){
    e.preventDefault();
    url = $(this).attr("data-href");
    $down_votes = $(this).parent().find("span.comment_down_votes_count")
    $up_votes = $(this).parent().find("span.comment_up_votes_count")
    console.log($down_votes.text())
    console.log($up_votes.text())
    $.get(url, function(response){
      if(response.status == "up"){
        count = parseInt($up_votes.text())
        $up_votes.text(count + 1);
      }
      else if(response.status == "removed"){
        count = parseInt($down_votes.text())
        $down_votes.text(count - 1);
      }
    });
  });
{% else %}
  $("#up_vote, #down_vote, #alert").click(function(){
    $("#alert").toggleClass("fade");
  });
{% endif %}