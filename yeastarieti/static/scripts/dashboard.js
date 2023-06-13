function showContactsDropdown() {
    var dropdown = document.getElementById("contactsDropdown");
    dropdown.classList.toggle("hidden");
}

function fillReceiver(number) {
    var receiverInput = document.getElementById("id_receiver");
    receiverInput.value = number;
}