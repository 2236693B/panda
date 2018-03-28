$( document ).ready(function() {
      $('#myModal').modal('hide');
      $('#myModal').on('hidden', function () {
        // Load up a new modal...
        $('#myModal1').modal('show')
      });
      $(".select2").select2({
        tags: true
      });
      $(".js-example-basic-single, .js-example-basic-single1").select2();
    });