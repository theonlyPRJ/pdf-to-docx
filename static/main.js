// Navigation logic
const navBtns = document.querySelectorAll('.nav-btn');
const views = document.querySelectorAll('.view');

navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Update active button
        navBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update active view
        const targetId = btn.getAttribute('data-target');
        views.forEach(view => {
            if (view.id === targetId) {
                view.classList.remove('hidden');
            } else {
                view.classList.add('hidden');
            }
        });
    });
});

// Monaco Editor Initialization
require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.43.0/min/vs' }});
require(['vs/editor/editor.main'], function() {
    window.editor = monaco.editor.create(document.getElementById('monaco-editor'), {
        value: '# Hello PDF-to-DOCX Studio\n\nThis is a sample document.\n\n## Math Equation\n\nInline math: $\\alpha^2 + \\beta^2 = \\gamma^2$\n\nDisplay math:\n$$\\int_{a}^{b} x^2 dx$$\n',
        language: 'markdown',
        theme: 'vs-dark',
        fontFamily: "'Fira Code', monospace",
        fontSize: 14,
        minimap: { enabled: false },
        wordWrap: 'on',
        padding: { top: 16 }
    });
    
    // Auto-resize
    window.addEventListener('resize', () => {
        window.editor.layout();
    });
});

// Compilation Logic
const compileBtn = document.getElementById('compile-btn');
const compileStatus = document.getElementById('compile-status');

compileBtn.addEventListener('click', async () => {
    const markdown = window.editor.getValue();
    compileStatus.className = 'status-box loading';
    compileStatus.innerHTML = '<p>Compiling to DOCX...</p>';

    const formData = new FormData();
    formData.append('markdown', markdown);

    try {
        const response = await fetch('/api/compile', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'compiled.docx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            
            compileStatus.className = 'status-box success';
            compileStatus.innerHTML = '<p>Compilation successful! File downloaded.</p>';
        } else {
            const err = await response.json();
            compileStatus.className = 'status-box error';
            compileStatus.innerHTML = `<p>Error: ${err.error}</p>`;
        }
    } catch (error) {
        compileStatus.className = 'status-box error';
        compileStatus.innerHTML = `<p>Error: ${error.message}</p>`;
    }
});

// PDF Conversion Logic
const dropZone = document.getElementById('drop-zone');
const pdfUpload = document.getElementById('pdf-upload');
const uploadStatus = document.getElementById('upload-status');

dropZone.addEventListener('click', () => pdfUpload.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
        handleUpload(e.dataTransfer.files[0]);
    }
});

pdfUpload.addEventListener('change', (e) => {
    if (e.target.files.length) {
        handleUpload(e.target.files[0]);
    }
});

async function handleUpload(file) {
    if (!file.name.endsWith('.pdf')) {
        uploadStatus.className = 'status-box error';
        uploadStatus.innerHTML = '<p>Please upload a valid PDF file.</p>';
        return;
    }

    uploadStatus.className = 'status-box loading';
    uploadStatus.innerHTML = `<p>Converting ${file.name} to DOCX...</p>`;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = file.name.replace('.pdf', '.docx');
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);

            uploadStatus.className = 'status-box success';
            uploadStatus.innerHTML = `<p>Conversion successful! ${a.download} downloaded.</p>`;
        } else {
            const err = await response.json();
            uploadStatus.className = 'status-box error';
            uploadStatus.innerHTML = `<p>Error: ${err.error || 'Unknown error'}</p>`;
        }
    } catch (error) {
        uploadStatus.className = 'status-box error';
        uploadStatus.innerHTML = `<p>Error: ${error.message}</p>`;
    }
}
