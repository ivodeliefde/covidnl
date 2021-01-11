
if ($(window).width() < 1200){
    document.getElementById("button_container").classList.add('col');
    document.getElementById("button_container").classList.remove('row');
} else {
    document.getElementById("button_container").classList.add('row');
    document.getElementById("button_container").classList.remove('col');
}
