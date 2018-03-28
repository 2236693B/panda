$('.delete-category').click(function(e){
  e.preventDefault();
  href = $(this).attr('data-href');
  if (!confirm('Do you want to delete Category?'))
    return;
  $.post(href, $("form#jobform").serialize(), function(data) {
          if (data.error) {
            alert(data.response);
          } else {
            alert("Category Deleted Successfully")
            window.location = '.';
          }
        }, 'json');
  });