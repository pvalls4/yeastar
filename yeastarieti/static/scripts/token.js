function tokenReveal() {
    var parrafo = document.getElementById("token");
    parrafo.textContent = token;
    parrafo.onclick = function() {tokenHide();}
}
function tokenHide() {
    var parrafo = document.getElementById("token");
    parrafo.textContent = "Pulsa para desvelar el token";
    parrafo.onclick = function() {tokenReveal();}
}

function copyToClipboard(value) {
    navigator.clipboard.writeText(value)
}

document.getElementById("copy-button").addEventListener("click", function() {
    copyToClipboard(token)

    // Mostrar una notificación o mensaje de éxito
    var originalImage = this.querySelector("img").src;
    this.querySelector("img").src = tickImage;
    this.querySelector("img").alt = "Copiado";
    this.title = "Copiado en el portapapeles";

    setTimeout(function() {
        // Restaurar la imagen original después de 2 segundos
        this.querySelector("img").src = originalImage;
        this.querySelector("img").alt = "Copiar";
        this.title = "Copiar en el portapapeles";
    }.bind(this), 1500);
});
