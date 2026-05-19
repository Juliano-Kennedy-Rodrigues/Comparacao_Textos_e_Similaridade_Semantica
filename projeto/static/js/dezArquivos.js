const dropZone = document.getElementById("drop-zone");
const dropZone2 = document.getElementById("drop-zone2");
const preview = document.getElementById("preview");
const fileInput = document.getElementById("file-input");
const fileInput2 = document.getElementById("file-input2")
const clearBtn = document.getElementById("clear-btn");

const allowedTypes = ["text/plain", "application/pdf"];
const MAX_FILES = 6; 
var fileInput_number = 0;

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

  if (fileInput_number == 1){
    alert(`Operação cancelada! Apenas um arquivo principal pode ser comparado com os outros arquivos por vez.`);
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
  }

}


function dropHandler(ev) {
    ev.preventDefault();
    ev.stopPropagation();
    
    const files = ev.dataTransfer.files; 
    displayFiles(files);
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
});

dropZone2.addEventListener("drop", (e) => {
    dropZone2.classList.remove("drag-over");
    dropHandler(e);
});

fileInput.addEventListener("change", (e) => {
    displayFiles(e.target.files);
    fileInput_number++;
    alert('colocou principal')

});

fileInput2.addEventListener("change", (e) => {
    displayFiles(e.target.files);
});

clearBtn.addEventListener("click", () => {
    preview.innerHTML = "";
    fileInput.value = "";
    fileInput2.value = "";
});