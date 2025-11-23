// Validación y animaciones para index.html

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const nombre = document.getElementById('nombre');
    const correo = document.getElementById('correo');
    const telefono = document.getElementById('telefono');

    form.addEventListener('submit', function (e) {
        let valid = true;
        let msg = '';
        if (nombre.value.trim().length < 3) {
            valid = false;
            msg = 'El nombre debe tener al menos 3 caracteres.';
        } else if (!correo.value.match(/^\S+@\S+\.\S+$/)) {
            valid = false;
            msg = 'Correo electrónico inválido.';
        }
        if (!valid) {
            e.preventDefault();
            mostrarMensaje(msg, false);
        } else {
            mostrarMensaje('Contacto guardado correctamente.', true);
        }
    });

    function mostrarMensaje(texto, exito) {
        let msgDiv = document.getElementById('form-msg');
        if (!msgDiv) {
            msgDiv = document.createElement('div');
            msgDiv.id = 'form-msg';
            form.appendChild(msgDiv);
        }
        msgDiv.textContent = texto;
        msgDiv.className = exito ? 'success-msg' : 'error-msg';
        setTimeout(() => { msgDiv.textContent = ''; }, 3000);
    }
});
