document.addEventListener("DOMContentLoaded", function(event) {
        $(function(){
            $('#example').popover({ trigger:'hover' });
        });
  });

  $('#deleteFeature').on('show.bs.modal', function(e) {

    var feature_id = $(e.relatedTarget).data('feature-id');
    var admin_link = "http://127.0.0.1:5000/admin/"
    $(e.currentTarget).find('a[name="confirm"]').attr("href", admin_link + "features/" + feature_id + "/delete");
  });

  $("#add-feature-cancel").on("click", function(e){
        $('#add-feature-form')[0].reset();
  });

  $("#add-feature-x").on("click", function(e){
        $('#add-feature-form')[0].reset();
  });