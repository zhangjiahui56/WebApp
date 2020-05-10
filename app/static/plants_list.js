document.addEventListener("DOMContentLoaded", function(event) {
        $(function(){
            $('#example').popover({ trigger:'hover' });
        });
  });

  $('#deletePlant').on('show.bs.modal', function(e) {

    //get data-id attribute of the clicked element
    var plant_id = $(e.relatedTarget).data('plant-id');
    //populate the textbox
    var admin_link = "http://127.0.0.1:5000/admin/"
    $(e.currentTarget).find('a[name="confirm"]').attr("href", admin_link + "plants/" + plant_id + "/delete");
  });

  $('#editPlant').on('show.bs.modal', function(e) {

    //get data-id attribute of the clicked element
    var plant_id = $(e.relatedTarget).data('plant-id');
    //populate the textbox

    $(e.currentTarget).find('input[id="plant_id"]').val(plant_id);
    $(e.currentTarget).find('div[id="plant_id"]').text("ID: "+plant_id);
  });

  $('#addPhase').on('show.bs.modal', function(e) {

    //get data-id attribute of the clicked element
    var plant_id = $(e.relatedTarget).data('plant-id');
    var zip_plant_name = $(e.relatedTarget).data.Zip;
    var plant_name = $(e.relatedTarget).data('plant-name');
    console.log(plant_name);
    //populate the textbox

    $(e.currentTarget).find('input[id="plant_id"]').val(plant_id);
    $(e.currentTarget).find('div[id="plant_name"]').text("Plant: "+plant_name);
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