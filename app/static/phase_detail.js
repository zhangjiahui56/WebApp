document.addEventListener("DOMContentLoaded", function(event) {
        $(function(){
            $('#example').popover({ trigger:'hover' });
        });
  });

$('#deletePhaseFeature').on('show.bs.modal', function(e) {
    var phase_id = $(e.relatedTarget).data('phase-id');
    var feature_id = $(e.relatedTarget).data('feature-id');
    var admin_link = "http://127.0.0.1:5000/admin/";
    $(e.currentTarget).find('a[name="confirm"]').attr("href", admin_link + "phase/" + phase_id + "/delete_feature/" + feature_id);
  });