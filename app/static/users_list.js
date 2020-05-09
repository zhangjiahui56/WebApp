document.addEventListener("DOMContentLoaded", function(event) {
        $(function(){
            $('#example').popover({ trigger:'hover' });
        });
  });
  $('#deleteUserModal').on('show.bs.modal', function(e) {

    //get data-id attribute of the clicked element
    var user_id = $(e.relatedTarget).data('user-id');
    //populate the textbox
    var admin_link = "http://127.0.0.1:5000/admin/"
    $(e.currentTarget).find('a[name="confirm"]').attr("href", admin_link + "user/" + user_id + "/delete");
  });
  $('#editUser').on('show.bs.modal', function(e) {

    //get data-id attribute of the clicked element
    var user_id = $(e.relatedTarget).data('user-id');
    var username = $(e.relatedTarget).data('username')
    //populate the textbox

    $(e.currentTarget).find('input[id="user_id"]').val(user_id)
    $(e.currentTarget).find('input[id="username"]').val(username)
    $(e.currentTarget).find('div[id="user_id"]').text("ID: "+user_id)
    $(e.currentTarget).find('div[id="username"]').text("Username: "+username)
  });

  $("#edit-cancel").on("click", function(e){
        $('#edit-form')[0].reset();
  });

  $("#add-cancel").on("click", function(e){
        $('#add-form')[0].reset();
  });