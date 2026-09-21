const dropZone = document.getElementById("drop-zone");
const dropZone2 = document.getElementById("drop-zone2");
const preview = document.getElementById("preview");
const fileInput = document.getElementById("file-input");
const fileInput2 = document.getElementById("file-input2");
const clearBtn = document.getElementById("clear-btn");

const allowedTypes = ["text/plain", "application/pdf"];
const MAX_FILES = 10; // 1 Principal + até 9 para comparação

// Acumuladores independentes para cada caixa
let principalDT = new DataTransfer();
let comparacaoDT = new DataTransfer();

function validarArquivo(file) {
    const extensaoValida = file.name.toLowerCase().endsWith(".txt") || file.name.toLowerCase().endsWith(".pdf");
    return allowedTypes.includes(file.type) || extensaoValida;
}

function atualizarPreview() {
    preview.innerHTML = "";

    if (principalDT.files.length > 0) {
        const file = principalDT.files[0];
        const li = document.createElement("li");
        li.className = "file-wrapper";
        li.innerHTML = `
            <div class="file-item">
                <span class="file-icon">${file.name.toLowerCase().endsWith(".pdf") ? "📄" : "📝"}</span>
                <span class="file-name">${file.name}</span> <strong style="color: #007bff;">(Principal)</strong>
            </div>
        `;
        preview.appendChild(li);
    }

    for (let i = 0; i < comparacaoDT.files.length; i++) {
        const file = comparacaoDT.files[i];
        const li = document.createElement("li");
        li.className = "file-wrapper";
        li.innerHTML = `
            <div class="file-item">
                <span class="file-icon">${file.name.toLowerCase().endsWith(".pdf") ? "📄" : "📝"}</span>
                <span class="file-name">${file.name}</span>
            </div>
        `;
        preview.appendChild(li);
    }
}

function adicionarPrincipal(files) {
    if (files.length === 0) return;

    const file = files[0]; // Aceita apenas 1 como principal
    if (!validarArquivo(file)) {
        alert(`O ficheiro "${file.name}" não é válido. Aceites apenas .txt e .pdf.`);
        return;
    }

    // Substitui o ficheiro principal anterior, se existir
    principalDT = new DataTransfer();
    principalDT.items.add(file);
    atualizarPreview();
}

function adicionarComparacao(files) {
    const fileArray = Array.from(files);

    const totalAtual = principalDT.files.length + comparacaoDT.files.length;
    if (totalAtual + fileArray.length > MAX_FILES) {
        alert(`Operação cancelada! O limite total é de ${MAX_FILES} ficheiros (1 principal + até 9 de comparação).`);
        return;
    }

    for (const file of fileArray) {
        if (!validarArquivo(file)) {
            alert(`O ficheiro "${file.name}" não é válido. Aceites apenas .txt e .pdf.`);
            return;
        }
    }

    for (const file of fileArray) {
        comparacaoDT.items.add(file);
    }

    atualizarPreview();
}

async function enviarParaComparacao() {
    const files = [...principalDT.files, ...comparacaoDT.files];

    if (principalDT.files.length === 0) {
        alert("Por favor, adicione 1 ficheiro principal na primeira caixa.");
        return;
    }

    if (comparacaoDT.files.length === 0) {
        alert("Por favor, adicione pelo menos 1 ficheiro para comparação na segunda caixa.");
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('arquivos', files[i]);
    }

    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrftoken = csrfInput ? csrfInput.value : '';

    try {
        const response = await fetch('/comparar/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            const resultadoDiv = document.getElementById("previewsHere");
            if (resultadoDiv) {
                resultadoDiv.innerHTML = "<h3>Resultados da Similaridade Semântica</h3>";

                data.resultados.forEach(item => {
                    resultadoDiv.innerHTML += `
                        <div class="resultado-item" style="margin-bottom: 10px; padding: 10px; border-left: 4px solid #007bff; background: #f9f9f9;">
                            <p style="margin: 0;"><strong>Âncora:</strong> ${item.Artigo_Ancora}</p>
                            <p style="margin: 0;"><strong>Comparado:</strong> ${item.Artigo_Comparado}</p>
                            <p style="margin: 5px 0 0 0; color: #28a745; font-weight: bold;">Similaridade: ${item.Similaridade}</p>
                        </div>
                    `;
                });
            }
        } else {
            alert("Erro no processamento: " + data.error);
        }
    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Ocorreu um erro ao enviar os ficheiros para comparação.");
    }
}

// Event Listeners - Drag and Drop
[dropZone, dropZone2].forEach(zone => {
    zone.addEventListener("dragover", (e) => {
        e.preventDefault();
        zone.classList.add("drag-over");
    });
    zone.addEventListener("dragleave", () => zone.classList.remove("drag-over"));
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
    adicionarPrincipal(e.dataTransfer.files);
});

dropZone2.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone2.classList.remove("drag-over");
    adicionarComparacao(e.dataTransfer.files);
});

fileInput.addEventListener("change", (e) => {
    adicionarPrincipal(e.target.files);
    fileInput.value = ""; 
});

fileInput2.addEventListener("change", (e) => {
    adicionarComparacao(e.target.files);
    fileInput2.value = "";
});

// Botão Limpar
clearBtn.addEventListener("click", () => {
    principalDT = new DataTransfer();
    comparacaoDT = new DataTransfer();
    fileInput.value = "";
    fileInput2.value = "";
    preview.innerHTML = "";

    const resultadoDiv = document.getElementById("previewsHere");
    if (resultadoDiv) {
        resultadoDiv.innerHTML = '<ul id="preview"></ul>';
    }
});