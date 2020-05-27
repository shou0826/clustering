
$(document).ready(function(){
    $("#upload-area").on("dragover", function(e){
        e.preventDefault();
    });
    $("#upload-area").on("drop", function(e){
        e.preventDefault();
        document.getElementById("id_file").files = e.originalEvent.dataTransfer.files;
    });
});