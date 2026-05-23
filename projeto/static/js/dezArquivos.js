const dropZone = document.getElementById("drop-zone");
const dropZone2 = document.getElementById("drop-zone2");
const preview = document.getElementById("preview");
const fileInput = document.getElementById("file-input");
const fileInput2 = document.getElementById("file-input2")
const clearBtn = document.getElementById("clear-btn");

const allowedTypes = ["text/plain", "application/pdf"];
const MAX_FILES = 10; 
var fileInput_number = 0;
var controle = 0;

function displayFiles(files) {
    const fileArray = Array.from(files);
    const jaExistentes = preview.querySelectorAll("li").length;
    const totalTentativa = jaExistentes + fileArray.length;

    if (totalTentativa > MAX_FILES) {
        alert(`Operação cancelada! Você tentou colocar ${fileArray.length} arquivo(s), mas o limite total é de ${MAX_FILES}. Limpe a lista ou selecione menos arquivos.`);
        fileInput.value = ""; 
        fileInput2.value = "";
        return; 
    }

    const todosSaoValidos = fileArray.every(file => 
        allowedTypes.includes(file.type) || file.name.toLowerCase().endsWith(".txt")
    );

    if (!todosSaoValidos) {
        alert("Operação cancelada! Um ou mais arquivos selecionados não são TXT ou PDF.");
        fileInput.value = "";
        fileInput2.value = "";
        return;
    }


    for (const file of fileArray) {

        const li = document.createElement("li");
        li.className = "file-wrapper";

        li.innerHTML = `
            <div class="file-item">
            <span class="file-icon">${file.name.toLowerCase().endsWith(".pdf") ? "📄" : "📝"}</span>
            <span class="file-name">${file.name}</span>
            </div>
        `;

        preview.appendChild(li);
        console.log(preview.children)

    }
}

function dropHandler(ev) {
    ev.preventDefault();
    ev.stopPropagation();
    
    const files = ev.dataTransfer.files; 
    displayFiles(files);
}

async function enviarParaComparacao() {
    const fileInput = document.getElementById("file-input");
    const files = [...fileInput.files, ...fileInput2.files];    

    if (files.length < 2) {
        alert("Por favor, selecione pelo menos 2 arquivos para comparar.");
        return;
    }

    const formData = new FormData();
    
    for (let i = 0; i < files.length; i++) {
        formData.append('arquivos', files[i]);
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
        const response = await fetch('/comparar/', { // URL que vamos criar no Django
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        });

        const data = await response.json();
        if (response.ok) {

            console.log("Dados recebidos do Django:", data.resultados);


            const resultadoDiv = document.getElementById("previewsHere"); 
            
            if (resultadoDiv) {
                resultadoDiv.innerHTML = "<h3>Resultados da Similaridade (BERTimbau)</h3>";

                // 3. Faz um loop pelos resultados e cria o HTML para cada comparação
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
                console.error("Erro: Não encontrei a div com id='resultado' no HTML.");
            }

        } else {
            alert("Erro no processamento: " + data.error);
        }
    } catch (error) {
        console.error("Erro na requisição:", error);
    }
}

// Listeners essenciais
dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drag-over");
});

dropZone2.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone2.classList.add("drag-over");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("drag-over");
});

dropZone2.addEventListener("dragleave", () => {
    dropZone2.classList.remove("drag-over");
});

dropZone.addEventListener("drop", (e) => {
    dropZone.classList.remove("drag-over");
    dropHandler(e);

    if (fileInput_number >= 1){
        alert(`Operação cancelada! Apenas um arquivo principal pode ser comparado com os outros arquivos por vez.`);
        fileInput.value = ""; 
        fileInput2.value = "";
        console.log(fileInput.value)
        return;
    }

    fileInput_number++;
});

dropZone2.addEventListener("drop", (e) => {
    dropZone2.classList.remove("drag-over");
    dropHandler(e);
    controle++
});

fileInput.addEventListener("change", (e) => {
    displayFiles(e.target.files);
    if (fileInput_number >= 1){
        alert(`Operação cancelada! Apenas um arquivo principal pode ser comparado com os outros arquivos por vez.`);
        console.log(fileInput_number)
        preview.children[fileInput_number + controle].innerHTML = "";
        fileInput.value = ""; 
        fileInput2.value = "";
        console.log(fileInput.value)
        fileInput_number++;
        return;
    }
    fileInput_number++;
    alert(fileInput_number)
});

fileInput2.addEventListener("change", (e) => {
    displayFiles(e.target.files);
    controle++;
});

clearBtn.addEventListener("click", () => {
    preview.innerHTML = "";
    fileInput.value = "";
    fileInput2.value = "";
    fileInput_number = 0

    const resultadoDiv = document.getElementById('previewsHere')
    if (resultadoDiv) {
        console.log("Limpando conteúdo antigo:", resultadoDiv.innerHTML);
        resultadoDiv.innerHTML = "";
    }
});


