$('#deleteImage').on('show.bs.modal', function(e) {

    //get data-id attribute of the clicked element
    var image_id = $(e.relatedTarget).data('image-id');
    //populate the textbox
    var admin_link = "http://127.0.0.1:5000/admin/"
    $(e.currentTarget).find('a[name="confirm"]').attr("href", admin_link + "images/" + image_id + "/delete");
});