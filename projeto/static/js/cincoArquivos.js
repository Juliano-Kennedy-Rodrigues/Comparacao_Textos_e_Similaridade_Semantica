const dropZone = document.getElementById("drop-zone");
const preview = document.getElementById("preview");
const fileInput = document.getElementById("file-input");
const clearBtn = document.getElementById("clear-btn");

const allowedTypes = ["text/plain", "application/pdf"];
const MAX_FILES = 5; 

function displayFiles(files) {
  const fileArray = Array.from(files);
  const jaExistentes = preview.querySelectorAll("li").length;
  const totalTentativa = jaExistentes + fileArray.length;

  if (totalTentativa > MAX_FILES) {
    alert(`Operação cancelada! Você tentou colocar ${fileArray.length} arquivo(s), mas o limite total é de ${MAX_FILES}. Limpe a lista ou selecione menos arquivos.`);
    fileInput.value = ""; 
    return; 
  }

  const todosSaoValidos = fileArray.every(file => 
    allowedTypes.includes(file.type) || file.name.toLowerCase().endsWith(".txt")
  );

  if (!todosSaoValidos) {
    alert("Operação cancelada! Um ou mais arquivos selecionados não são TXT ou PDF.");
    fileInput.value = "";
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

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("drag-over");
});

dropZone.addEventListener("drop", (e) => {
    dropZone.classList.remove("drag-over");
    dropHandler(e);
});

fileInput.addEventListener("change", (e) => {
    displayFiles(e.target.files);
});

clearBtn.addEventListener("click", () => {
    preview.innerHTML = "";
    fileInput.value = "";
});