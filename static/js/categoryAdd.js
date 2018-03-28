$('form#categoryform').submit(function(e){
	e.preventDefault();
	$("input[name='description']").val(CKEDITOR.instances.textareacontents.getData());
	$.post('.', $('form#categoryform').serialize(), function(data){
	      	console.log(data)
	      	console.log(data.error)
	        if (data.error == false) {
	          alert(data.response);
	          window.location = "{% url 'categories' %}";
	        } else {
	          $('div.error').remove();
	          for (var key in data.response) {
	            $('#' + key).after('<div class="error">' + data.response[key] + '</div>');
	          }
	        }
	}, 'json');
});
$('.cancel').click(function(e){
	window.location = "{% url 'categories' %}";
});
   CKEDITOR.replace( 'textareacontents',
   {
   // toolbar :
   // [
   // { name: 'basicstyles', items : [ 'Bold','Italic' ] },
   // { name: 'paragraph', items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv',
   // '-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ] },
   // ],
   // skin : 'office2003',
   uiColor: '#ffffff',
     height:260,
   //width: 700,
   });