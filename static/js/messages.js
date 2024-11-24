$(document).ready(function() {
    setTimeout(function() {
        $(".messages li").fadeOut(1000, function() { 
            $(this).remove(); 
        });
    }, 3000); 
});
