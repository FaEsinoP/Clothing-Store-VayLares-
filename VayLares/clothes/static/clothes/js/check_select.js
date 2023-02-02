function enableButton()
{
    var selectelem = document.getElementById('select_size');
    var btnelem = document.getElementById('submit_button');
    btnelem.disabled = !selectelem.value;
}