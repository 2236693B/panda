b$("a[rel='page']").click(function(e){
          e.preventDefault();
          $('#filter_form').attr("action", $(this).attr("href"));
          $('#filter_form').submit();
        });
        $("#pagination_per_page").change(function(e) {
          var a = $("#pagination_per_page").val();
          $("#filter_per_page").val(a);
          $('#filter_form').submit();
        });
        $(document).ready(function(e){
          var pathname = window.location.pathname;
          atag = $('.menu a[href="'+pathname+'"]');
          atag.parent().addClass("active");
        });
        $(".select2").select2({
        tags: true
      });