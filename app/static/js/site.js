$(document).ready(function(){
 $( "#id_file" ).on( 'change', function updateFileName( event ){
    var input = $( this );
    var label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    $("#id_file_name").text(label);
    });
});
