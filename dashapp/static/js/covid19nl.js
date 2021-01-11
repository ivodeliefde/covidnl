
adjustLayout = function(){
    if ($(window).width() < 1200){
        console.log("Optimize layout for small screen size: "+$(window).width())
        $('#button_container').addClass('row').removeClass('col');
    } else {
        console.log("Optimize layout for large screen size: "+$(window).width())
        $('#button_container').addClass('col').removeClass('row');
    }
};

window.addEventListener('load', adjustLayout);
window.addEventListener('DOMContentLoaded', adjustLayout);
window.addEventListener('online', adjustLayout);
window.addEventListener('resize', adjustLayout);
