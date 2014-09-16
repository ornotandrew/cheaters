$(document).ready(function(){
 $( "#id_file" ).on( 'change', function updateFileName( event ){
    var input = $( this );
    var label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    $("#id_file_name").text(label);
    });
});

//Callback handler for form submit event
$(document).ready(function(){
    $("#uploadform").submit(function(e)
    {

        var formObj = $(this);
        var formURL = formObj.attr("action");
        var formData = new FormData(this);
        $.ajax({
            url: formURL,
            type: 'POST',
            data:  formData,
            mimeType:"multipart/form-data",
            contentType: false,
            cache: false,
            processData:false,
        success: function(response)
        {
            var report_id = $.parseJSON(response).report_id
            window.open("/report/"+report_id, "_blank");
        },
         error: function(response)
         {
            console.log("failure")
         }
        });
        e.preventDefault(); //Prevent Default action.

    });
});
$("#uploadform").submit(); //Submit the form
