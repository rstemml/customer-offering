/**
 * Customer Offering Generator - Frontend Logic
 * Philosophy: Simple, functional, elegant
 */

// ==================== State ====================
let currentData = null;
let currentYaml = null;

// ==================== Mode Switching ====================
document.querySelectorAll('.mode-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Update active state
        document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Show selected mode content
        const mode = btn.dataset.mode;
        document.querySelectorAll('.mode-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${mode}-mode`).classList.add('active');

        // Hide preview and success sections
        hidePreview();
        hideSuccess();
    });
});

// ==================== Chat Extraction ====================
document.getElementById('extract-btn').addEventListener('click', async () => {
    const text = document.getElementById('chat-input').value.trim();

    if (!text) {
        showError('Bitte geben Sie Text ein.');
        return;
    }

    const btn = document.getElementById('extract-btn');
    setLoading(btn, true);

    try {
        const response = await fetch('/api/extract', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Extraction failed');
        }

        currentData = result.data;
        currentYaml = result.yaml;

        showPreview();
        await calculatePricing();

    } catch (error) {
        showError(`Fehler beim Extrahieren: ${error.message}`);
    } finally {
        setLoading(btn, false);
    }
});

// ==================== File Upload ====================
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');

uploadArea.addEventListener('click', () => {
    fileInput.click();
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--primary-color)';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = 'var(--border-color)';
});

uploadArea.addEventListener('drop', async (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--border-color)';

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        await handleFileUpload(files[0]);
    }
});

fileInput.addEventListener('change', async (e) => {
    const files = e.target.files;
    if (files.length > 0) {
        await handleFileUpload(files[0]);
    }
});

async function handleFileUpload(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Upload failed');
        }

        // Show file info
        const fileInfo = document.getElementById('file-info');
        fileInfo.innerHTML = `✓ Datei geladen: <strong>${file.name}</strong>`;
        fileInfo.style.display = 'block';

        currentData = result.data;
        currentYaml = result.yaml;

        showPreview();
        await calculatePricing();

    } catch (error) {
        showError(`Fehler beim Hochladen: ${error.message}`);
    }
}

// ==================== Manual Entry ====================
document.getElementById('parse-btn').addEventListener('click', async () => {
    const yamlText = document.getElementById('manual-input').value.trim();

    if (!yamlText) {
        showError('Bitte geben Sie YAML-Daten ein.');
        return;
    }

    const btn = document.getElementById('parse-btn');
    setLoading(btn, true);

    try {
        // Parse YAML
        currentData = parseYAML(yamlText);
        currentYaml = yamlText;

        showPreview();
        await calculatePricing();

    } catch (error) {
        showError(`Fehler beim Parsen: ${error.message}`);
    } finally {
        setLoading(btn, false);
    }
});

// ==================== Tab Switching ====================
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const tab = btn.dataset.tab;
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tab}-tab`).classList.add('active');
    });
});

// ==================== Preview ====================
function showPreview() {
    document.getElementById('preview-yaml').value = currentYaml;
    document.getElementById('preview-section').style.display = 'block';

    // Scroll to preview
    document.getElementById('preview-section').scrollIntoView({ behavior: 'smooth' });
}

function hidePreview() {
    document.getElementById('preview-section').style.display = 'none';
}

// ==================== Calculate Pricing ====================
document.getElementById('calculate-btn').addEventListener('click', calculatePricing);

async function calculatePricing() {
    try {
        // Get current YAML from preview
        const yamlText = document.getElementById('preview-yaml').value;

        // Parse YAML (simple parsing, could fail)
        const data = parseYAML(yamlText);

        const response = await fetch('/api/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Validation failed');
        }

        // Display pricing
        displayPricing(result);

        currentData = data;

    } catch (error) {
        showError(`Fehler bei der Kalkulation: ${error.message}`);
    }
}

function displayPricing(result) {
    const { pricing, team_costs, team_size } = result;

    let html = `
        <h3>Team Kosten</h3>
        <div class="team-costs">
    `;

    team_costs.forEach(tc => {
        html += `
            <div class="team-cost">
                <strong>${tc.role}</strong> (${tc.count}x):
                ${formatCurrency(tc.subtotal)}
            </div>
        `;
    });

    html += `
        </div>
        <h3>Zusammenfassung</h3>
        <div>Zwischensumme: ${formatCurrency(pricing.subtotal)}</div>
        <div>Rabatt (${pricing.discount_percent}%): -${formatCurrency(pricing.discount_amount)}</div>
        <div>Nach Rabatt: ${formatCurrency(pricing.subtotal_after_discount)}</div>
        <div>MwSt. (${pricing.tax_percent}%): ${formatCurrency(pricing.tax_amount)}</div>
        <div class="total">GESAMT: ${pricing.total_formatted}</div>
    `;

    document.getElementById('pricing-display').innerHTML = html;

    // Switch to pricing tab
    document.querySelector('.tab-btn[data-tab="pricing"]').click();
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('de-DE', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

// ==================== Generate PowerPoint ====================
document.getElementById('generate-btn').addEventListener('click', async () => {
    if (!currentData) {
        showError('Bitte zuerst Daten extrahieren oder hochladen.');
        return;
    }

    const btn = document.getElementById('generate-btn');
    setLoading(btn, true);

    try {
        // Get updated YAML from preview
        const yamlText = document.getElementById('preview-yaml').value;
        const data = parseYAML(yamlText);

        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Generation failed');
        }

        // Show success
        showSuccess(result);

    } catch (error) {
        showError(`Fehler beim Generieren: ${error.message}`);
    } finally {
        setLoading(btn, false);
    }
});

// ==================== Success ====================
function showSuccess(result) {
    document.getElementById('success-message').textContent =
        `Datei: ${result.filename}`;

    const downloadLink = document.getElementById('download-link');
    downloadLink.href = result.download_url;
    downloadLink.download = result.filename;

    document.getElementById('success-section').style.display = 'block';
    hidePreview();

    // Scroll to success
    document.getElementById('success-section').scrollIntoView({ behavior: 'smooth' });
}

function hideSuccess() {
    document.getElementById('success-section').style.display = 'none';
}

document.getElementById('new-offer-btn').addEventListener('click', () => {
    location.reload();
});

// ==================== Error Handling ====================
function showError(message) {
    document.getElementById('error-message').textContent = message;
    document.getElementById('error-display').style.display = 'block';

    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    document.getElementById('error-display').style.display = 'none';
}

document.getElementById('close-error').addEventListener('click', hideError);

// ==================== Utilities ====================
function setLoading(button, isLoading) {
    const text = button.querySelector('.btn-text');
    const loader = button.querySelector('.btn-loader');

    if (isLoading) {
        text.style.display = 'none';
        loader.style.display = 'inline-block';
        button.disabled = true;
    } else {
        text.style.display = 'inline-block';
        loader.style.display = 'none';
        button.disabled = false;
    }
}

function parseYAML(yamlText) {
    try {
        // Try to parse as JSON first (if user enters JSON)
        return JSON.parse(yamlText);
    } catch {
        // Parse as YAML using js-yaml library
        try {
            return jsyaml.load(yamlText);
        } catch (error) {
            throw new Error(`YAML parsing error: ${error.message}`);
        }
    }
}
