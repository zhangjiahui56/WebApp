var btnUpload = $("#upload_file"),
        btnOuter = $(".button_outer");
    btnUpload.on("change", function(e){
        var ext = btnUpload.val().split('.').pop().toLowerCase();
        if($.inArray(ext, ['gif','png','jpg','jpeg']) == -1) {
            $(".error_msg").text("Not an Image...");
        } else {
            $(".error_msg").text("");
            btnOuter.addClass("file_uploading");
            setTimeout(function(){
                btnOuter.addClass("file_uploaded");
            },3000);
            var uploadedFile = URL.createObjectURL(e.target.files[0]);
            setTimeout(function(){
                $("#uploaded_view").append('<img src="'+uploadedFile+'" />').addClass("show");

                $("#form-upload").append('<button type="submit" class="btn btn-primary" style="display: block; margin: 0 auto;font-size: 2rem;background-color:#70c745;border-color:#70c745;border-radius: 6px;">Upload</button>');
            },3500);
        }
    });
    $(".file_remove").on("click", function(e){
        $("#uploaded_view").removeClass("show");
        $("#uploaded_view").find("img").remove();
        $("#upload_file").val('');
        $("#form-upload").find("button").remove();
        btnOuter.removeClass("file_uploading");
        btnOuter.removeClass("file_uploaded");
    });