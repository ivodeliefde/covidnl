
adjustLayout = function(){
    if ($(window).width() < 1200){
        console.log("Optimize layout for small screen")
        $('#button_container').addClass('row').removeClass('col');
    } else {
        console.log("Optimize layout for large screen")
        $('#button_container').addClass('col').removeClass('row');
    }
};

$(document).ready(adjustLayout);
window.addEventListener('load', adjustLayout);
window.addEventListener('resize', adjustLayout);
adjustLayout();