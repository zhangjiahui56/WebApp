document.addEventListener("DOMContentLoaded", function(event) {
        $(function(){
            $('#example').popover({ trigger:'hover' });
        });
  });

  $('#deletePlant').on('show.bs.modal', function(e) {

    //get data-id attribute of the clicked element
    var plant_id = $(e.relatedTarget).data('plant-id');
    //populate the textbox
    var admin_link = "http://127.0.0.1:5000/admin/";
    $(e.currentTarget).find('a[name="confirm"]').attr("href", admin_link + "plants/" + plant_id + "/delete");
  });

  $('#editPlant').on('show.bs.modal', function(e) {

    //get data-id attribute of the clicked element
    var plant_id = $(e.relatedTarget).data('plant-id');
    var plant_name = $(e.relatedTarget).data('plant-name');
    //populate the textbox

    $(e.currentTarget).find('input[id="plant_id"]').val(plant_id);
    $(e.currentTarget).find('input[id="edit-plant-name"]').val(plant_name);
    $(e.currentTarget).find('div[id="plant_id"]').text("ID: "+plant_id);
  });

  $('#addPhase').on('show.bs.modal', function(e) {

    //get data-id attribute of the clicked element
    var plant_id = $(e.relatedTarget).data('plant-id');
    var plant_name = $(e.relatedTarget).data('plant-name');
    //populate the textbox

    $(e.currentTarget).find('input[id="add-phase-plant_id"]').val(plant_id);
    $(e.currentTarget).find('div[id="add-phase-plant_name"]').text("Plant: "+plant_name);
  });

  $('#editPhase').on('show.bs.modal', function(e) {

    //get data-id attribute of the clicked element
    var plant_name = $(e.relatedTarget).data('plant-name');
    var phase_id = $(e.relatedTarget).data('phase-id');
    var phase_name = $(e.relatedTarget).data('phase-name');
    var phase_order = $(e.relatedTarget).data('phase-order');
    var phase_days = $(e.relatedTarget).data('phase-days');
    //populate the textbox

    $(e.currentTarget).find('input[id="edit-phase-id"]').val(phase_id);
    $(e.currentTarget).find('div[id="edit-phase-plant_name"]').text("Plant: "+plant_name);
    $(e.currentTarget).find('input[id="name"]').val(phase_name);
    $(e.currentTarget).find('input[id="order"]').val(phase_order);
    $(e.currentTarget).find('input[id="number_of_days"]').val(phase_days);
  });

  $('#deletePhase').on('show.bs.modal', function(e) {
    var phase_id = $(e.relatedTarget).data('phase-id');
    $(e.currentTarget).find('input[id="phase_id"]').val(phase_id);
    var admin_link = "http://127.0.0.1:5000/admin/"
    $(e.currentTarget).find('a[name="confirm"]').attr("href", admin_link + "phases/" + phase_id + "/delete");
  });

  $("#edit-cancel").on("click", function(e){
        $('#edit-form')[0].reset();
  });

  $("#add-cancel").on("click", function(e){
        $('#add-form')[0].reset();
  });

  $("#add-phase-cancel").on("click", function(e){
        $('#add-phase-form')[0].reset();
  });

  $("#edit-x").on("click", function(e){
        $('#edit-form')[0].reset();
  });

  $("#add-x").on("click", function(e){
    $('#add-form')[0].reset();
  });

  $("#add-phase-x").on("click", function(e){
    $('#add-phase-form')[0].reset();
  });

  $("#edit-phase-x").on("click", function(e){
        $('#edit-phase-form')[0].reset();
  });

  $("#edit-phase-cancel").on("click", function(e){
        $('#edit-phase-form')[0].reset();
  });