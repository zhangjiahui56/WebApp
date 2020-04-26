$("#edit").click(function(e){
        var name = $("#name").val();
        var address = $("#address").val();
        var phone_number = $("#phone_number").val();
        $("#name").removeAttr("disabled");
        $("#address").removeAttr("disabled");
        $("#phone_number").removeAttr("disabled");
        $("#submit-div").append('<button type="submit" id="edit-submit" class="btn btn-primary" value="Save Changes" style="font-size: 1.5rem;">Save Changes</button>');
        $("#submit-div").append('<span id="edit-span"> </span>');
        $("#submit-div").append('<input type="reset" id="edit-cancel" class="btn btn-secondary" value="Cancel" style="font-size: 1.5rem;">');
        $("#submit-div").find('#edit').hide();
        $("#edit-cancel").click(function() {
            $("#name").val(name);
            $("#address").val(address);
            $("#phone_number").val(phone_number);
            $("#name").attr('disabled', true);
            $("#address").attr('disabled', true);
            $("#phone_number").attr('disabled', true);
            $("#submit-div").find('#edit-submit').remove();
            $("#submit-div").find('#edit-span').remove();
            $("#submit-div").find('#edit-cancel').remove();
            $("#submit-div").find('#edit').show();
        });
    });