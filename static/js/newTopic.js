 $('.tags').tagsInput({width:'auto'});
   CKEDITOR.replace( 'description',
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
  

  $('form#newtopicform').submit(function(e){
        e.preventDefault();
        desc = CKEDITOR.instances.id_description.getData();
        $("[name='description']").val(desc);
        $.post('', $('form#newtopicform').serialize(), function(data){
          console.log(data)
	      	console.log(data.error)
	        if (data.error == false) {
	          alert(data.response);
	          window.location = "{% url 'topic_list' %}";
	        } else {
	          $('div.error').remove();
	          for (var key in data.response) {
	            $('#' + key).after('<div class="error">' + data.response[key] + '</div>');
	          }
	        }
        }, 'json');
      });
/*    $('#category').change(function(e){
      $('#sub_category').parent('div').removeClass('sub_category');
    });
*/