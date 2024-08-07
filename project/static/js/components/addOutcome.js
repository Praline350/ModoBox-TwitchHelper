function addForm() {
    var formIdx = document.querySelectorAll('.dynamic-form').length;
    var newForm = document.getElementById('form-empty').cloneNode(true);
    newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, formIdx);
    newForm.style.display = 'block';
    document.getElementById('outcome-forms').appendChild(newForm);
}