const dropZone = document.getElementById("drop-zone");
const preview = document.getElementById("preview");
const fileInput = document.getElementById("file-input");
const clearBtn = document.getElementById("clear-btn");

const allowedTypes = ["text/plain", "application/pdf"];
const MAX_FILES = 6; // 1 Principal + até 5 para comparação

let acumuladorArquivos = new DataTransfer();

function atualizarPreview() {
    // 1. Limpa o container visual
    preview.innerHTML = "";

    const arquivos = acumuladorArquivos.files;

    for (let i = 0; i < arquivos.length; i++) {
        const file = arquivos[i];
        const li = document.createElement("li");
        li.className = "file-wrapper";

        const ehPrincipal = (i === 0);
        const tagPrincipal = ehPrincipal ? ' <strong style="color: #007bff;">(Principal)</strong>' : '';

        li.innerHTML = `
            <div class="file-item" style="margin-bottom: 5px;">
                <span class="file-icon">${file.name.toLowerCase().endsWith(".pdf") ? "📄" : "📝"}</span>
                <span class="file-name">${file.name}</span>${tagPrincipal}
            </div>
        `;
        preview.appendChild(li);
    }

    fileInput.files = acumuladorArquivos.files;
}

function processarArquivosAdicionados(novosArquivos) {
    const fileArray = Array.from(novosArquivos);
    const totalFuturo = acumuladorArquivos.files.length + fileArray.length;

    if (totalFuturo > MAX_FILES) {
        alert(`Operação cancelada! O limite total é de ${MAX_FILES} arquivos (1 principal + 5 de comparação).`);
        return;
    }

    for (const file of fileArray) {
        const extensaoValida = file.name.toLowerCase().endsWith(".txt") || file.name.toLowerCase().endsWith(".pdf");
        if (!allowedTypes.includes(file.type) && !extensaoValida) {
            alert(`O arquivo "${file.name}" não é um formato válido (Apenas TXT ou PDF).`);
            return;
        }
    }

    // Adiciona os novos arquivos ao acumulador
    for (const file of fileArray) {
        acumuladorArquivos.items.add(file);
    }

    atualizarPreview();
}

async function enviarParaComparacao() {
    const files = acumuladorArquivos.files;

    if (files.length < 2) {
        alert("Por favor, selecione pelo menos 2 arquivos (1 principal e 1 para comparação).");
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
            let resultadoDiv = document.getElementById("resultado-container");
            if (!resultadoDiv) {
                resultadoDiv = document.createElement("div");
                resultadoDiv.id = "resultado-container";
                document.getElementById("secondDiv").appendChild(resultadoDiv);
            }

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
        } else {
            alert("Erro no processamento: " + data.error);
        }
    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Ocorreu um erro ao enviar os arquivos para comparação.");
    }
}

// Event Listeners
dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drag-over");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("drag-over");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
    if (e.dataTransfer.files.length > 0) {
        processarArquivosAdicionados(e.dataTransfer.files);
    }
});

fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
        processarArquivosAdicionados(e.target.files);
    }
    // Reseta o valor do input para permitir re-selecionar o mesmo arquivo se necessário
    fileInput.value = "";
});

clearBtn.addEventListener("click", () => {
    // Reseta o acumulador de arquivos
    acumuladorArquivos = new DataTransfer();
    fileInput.value = "";
    preview.innerHTML = "";

    const resultadoDiv = document.getElementById("resultado-container");
    if (resultadoDiv) {
        resultadoDiv.innerHTML = "";
    }
});