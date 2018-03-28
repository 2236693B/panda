$('.delete-topic').click(function(e){
  e.preventDefault();
  href = $(this).attr('data-href');
  if (!confirm('Do you want to delete Topic?'))
    return;
  $.post(href, $("form#jobform").serialize(), function(data) {
      if (data.error) {
        alert(data.response);
      } else {
        alert("Topic Deleted Successfully")
        window.location = '.';
      }
    }, 'json');
  });
  $('.topic-status').click(function(e){
  e.preventDefault();
  href = $(this).attr('data-href');
  if (!confirm('Do you want to change the status of topic?'))
    return;
  $.post(href, $("form#jobform").serialize(), function(data) {
      if (data.error) {
        alert(data.response);
      } else {
        alert("Topic Status Changed Successfully")
        window.location = '.';
      }
    }, 'json');
  });