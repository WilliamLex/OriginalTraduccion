let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3] },
        { orderable: false, targets: [0] },
        { searchable: false, targets: [1, 2, 3] }
    ],
    pageLength: 10,
    language: {
        lengthMenu: "Mostrar _MENU_ traducciones por página",
        zeroRecords: "Ninguna traducción encontrada",
        info: "Mostrando de _START_ a _END_ de un total de _TOTAL_ traducciones",
        infoEmpty: "Ninguna traducción encontrada",
        infoFiltered: "(filtrados desde _MAX_ traducciones totales)",
        search: "Buscar:",
        loadingRecords: "Cargando...",
        paginate: {
            first: "Primero",
            last: "Último",
            next: "Siguiente",
            previous: "Anterior"
        }
    }
};



const initDataTable = async (texto) => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await buscarTraduccion(texto);

    dataTable = $("#datatable-traducciones").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

const createTagWithOptions = (tagName, options) => {
    return Object.assign(document.createElement(tagName), options);
};

const buscarTraduccion = async (texto) => {
    const tipoTraduccionId = document.getElementById("cboTipoTraduccion").value;

    try {
        const response = await fetch(`${window.origin}/traductor/buscar_traduccion/${tipoTraduccionId}/${texto}`);
        const data = await response.json();

        if (data.mensaje === "exito") {
            document.getElementById("tableBody_Traducciones").innerHTML = ``;

            data.traducciones.forEach((traduccion, index) => {
                const tr = document.createElement("tr");

                tr.appendChild(createTagWithOptions("td", { innerText: index + 1 }));
                tr.appendChild(createTagWithOptions("td", { innerText: traduccion.tipo_traduccion__nombre }));
                tr.appendChild(createTagWithOptions("td", { innerText: traduccion.texto }));
                tr.appendChild(createTagWithOptions("td", { innerText: traduccion.texto_traducido }));

                document.getElementById("tableBody_Traducciones").appendChild(tr);
            });
        } else if (data.mensaje === "noencontradas") {
            document.getElementById("tableBody_Traducciones").innerHTML = ``;
        } else {
            alert("Ocurrió un error...");
        }
    } catch (ex) {
        alert("Ocurrió un error...");
    }
};



const speakTranslation = async () => {
    const textoTraducido = document.getElementById('txtTexto').value.trim();
    console.log('Texto Traducido:', textoTraducido);

    if (textoTraducido !== '') {
        // Crea una instancia de SpeechSynthesisUtterance y establece el idioma a inglés
        const utterance = new SpeechSynthesisUtterance();
        utterance.text = textoTraducido;
        utterance.lang = 'en-US';

        // Usar la síntesis de voz del navegador
        window.speechSynthesis.speak(utterance);
    } else {
        console.log('No hay texto traducido disponible.');
    }
};

const validarCampoTexto = () => {
    const campoTexto = document.getElementById('txtTexto');
    const valorCampo = campoTexto.value.trim();

    // Expresión regular que permite solo letras y espacios en blanco
    const soloTextoRegex = /^[A-Za-z\s]*$/;

    if (!soloTextoRegex.test(valorCampo)) {
        alert('Por favor, ingrese solo letras y espacios en blanco en el campo de texto.');
        campoTexto.value = ''; // Limpiar el campo si no cumple con los requisitos
        return false;
    }

    return true;
};

const validateInput = () => {
    return validarCampoTexto();
};

const validarFormulario = () => {
    if (!validateInput()) {
        return false; // Cancela el envío del formulario
    }

    // Resto de las validaciones o acciones del formulario

    return true; // Permite el envío del formulario
};

const initialLoad = () => {
    frmBusquedaTraduccion.addEventListener("submit", async (event) => {
        event.preventDefault();

        if (validarFormulario()) {
            await initDataTable(String(txtTexto.value).trim());
        }
    });

    document.getElementById('speakButton').addEventListener('click', speakTranslation);
};



window.addEventListener("load", () => {
    initialLoad();
});
