# Web UI Guide

**Eleganz trifft Benutzerfreundlichkeit.**

Die Web UI bietet eine moderne, intuitive Oberfläche für die Angebotsgenerierung. Keine Kommandozeile nötig. Einfach Browser öffnen und loslegen.

## Quick Start

```bash
# Install web dependencies
pip install -r requirements-web.txt

# Start server
python app.py
```

Öffne Browser: **http://localhost:5000**

## Features

### 3 Modi zur Auswahl

#### 1. 💬 **Chat Extraction**
Beschreiben Sie Ihr Angebot in natürlicher Sprache:

```
Erstelle Angebot für TechStart GmbH
Kontakt: Sarah Müller, sarah@techstart.de

Projekt: E-Commerce Platform
Dauer: 6 Monate
Start: 01.12.2025

Team:
- 1x Solution Architect, 1200 €/Tag
- 3x Senior Developer, 800 €/Tag

Deliverables:
- Architektur & Design
- Backend Development
- Testing & Deployment

Rabatt: 10%
```

**→ Daten werden automatisch extrahiert**

#### 2. 📁 **File Upload**
- Ziehen Sie eine YAML/JSON Datei in das Upload-Feld
- Oder klicken Sie zum Auswählen
- Datei wird automatisch geparst und validiert

**Unterstützte Formate:**
- `.yaml` / `.yml`
- `.json`

#### 3. 📝 **Manual Entry**
- Geben Sie YAML-Daten direkt ein
- Syntax-Highlighting
- Live-Validation

## Workflow

```
1. Wählen Sie einen Modus
   ↓
2. Geben Sie Daten ein (Text / Upload / YAML)
   ↓
3. Vorschau & Bearbeitung
   → YAML editieren
   → Preiskalkulation anzeigen
   ↓
4. PowerPoint Generieren
   ↓
5. Download fertige Präsentation
```

## UI Elemente

### Mode Selector
Drei große Buttons oben:
- Klicken um Modus zu wechseln
- Aktiver Modus ist blau hervorgehoben

### Chat Input
- Große Textarea für natürlichen Text
- Placeholder mit Beispieltext
- "Daten Extrahieren" Button

### Upload Area
- Drag & Drop Zone
- Click to select
- File info nach Upload

### YAML Editor
- Monospace Font
- Syntax-aware
- Direkt editierbar

### Preview Section
Zeigt nach Extraktion/Upload:
- **YAML Tab**: Editierbares YAML
- **Preiskalkulation Tab**:
  - Team Kosten Breakdown
  - Zwischensumme
  - Rabatt
  - MwSt
  - **Gesamt** (hervorgehoben)

### Action Buttons
- **💰 Preis Berechnen**: Update Kalkulation
- **✨ PowerPoint Generieren**: Erstellt Präsentation

### Success View
Nach erfolgreicher Generierung:
- 🎉 Success Icon
- Dateiname anzeigen
- **Download Button** (hervorgehoben)
- "Neues Angebot Erstellen" (lädt Seite neu)

## API Endpoints

Die Web UI kommuniziert mit folgenden Endpoints:

### `POST /api/extract`
Extrahiert Daten aus natürlichem Text.

**Request:**
```json
{
  "text": "Angebot für Acme Corp..."
}
```

**Response:**
```json
{
  "success": true,
  "data": { ... },
  "yaml": "customer:\n  name: Acme Corp\n..."
}
```

### `POST /api/validate`
Validiert und kalkuliert Preise.

**Request:**
```json
{
  "customer": { ... },
  "project": { ... },
  "team": [ ... ],
  ...
}
```

**Response:**
```json
{
  "success": true,
  "valid": true,
  "pricing": {
    "subtotal": 500000,
    "total": 632961.00,
    "total_formatted": "632 961.00 €"
  },
  "team_costs": [ ... ]
}
```

### `POST /api/generate`
Generiert PowerPoint Präsentation.

**Request:** Vollständige Offer-Daten

**Response:**
```json
{
  "success": true,
  "filename": "acme-corp-offer-2025-11-05.pptx",
  "download_url": "/api/download/acme-corp-offer-2025-11-05.pptx"
}
```

### `GET /api/download/<filename>`
Lädt generierte Datei herunter.

**Response:** Binary PowerPoint file

### `POST /api/upload`
Uploaded und parst YAML/JSON Datei.

**Request:** multipart/form-data mit file

**Response:** Wie `/api/extract`

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

## Design Philosophy

### Apple-Inspired
- Clean, minimalistisches Design
- Viel Weißraum
- Klare Typographie
- Smooth Transitions

### Color Scheme
- **Primary**: `#0066cc` (Professional Blue)
- **Background**: `#f5f5f7` (Light Gray)
- **Card**: `#ffffff` (White)
- **Text**: `#1d1d1f` (Near Black)
- **Secondary Text**: `#86868b` (Gray)

### Typography
```css
font-family: -apple-system, BlinkMacSystemFont,
             'Segoe UI', 'Roboto', 'Helvetica',
             'Arial', sans-serif
```

### Responsive
- Funktioniert auf Desktop, Tablet, Mobile
- Flexbox & Grid Layout
- Touch-friendly Buttons

## Technische Details

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling (Flexbox, Grid, Animations)
- **Vanilla JavaScript** - No framework needed
- **js-yaml** - YAML parsing (CDN)

### Backend
- **Flask** - Python web framework
- **Flask-CORS** - Cross-origin requests
- Integration mit existing `src/` modules

### File Structure
```
customer-offering/
├── app.py                  # Flask backend
├── requirements-web.txt    # Web dependencies
│
├── templates/
│   └── index.html          # Main UI
│
└── static/
    ├── css/
    │   └── style.css       # Styling
    └── js/
        └── app.js          # Frontend logic
```

## Development

### Start Development Server
```bash
python app.py
# Server runs on http://localhost:5000
# Debug mode enabled
# Auto-reload on file changes
```

### Configuration
In `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
UPLOAD_FOLDER = Path(tempfile.gettempdir()) / 'customer-offering-uploads'
```

### Error Handling
- Validation errors → Red banner with message
- Network errors → User-friendly message
- Auto-hide after 5 seconds
- Manual close button

### Loading States
- Buttons show spinner during operations
- Disabled during processing
- Clear feedback for user actions

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt requirements-web.txt ./
RUN pip install -r requirements.txt -r requirements-web.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Environment Variables
```bash
FLASK_ENV=production
FLASK_DEBUG=0
```

### Reverse Proxy (nginx)
```nginx
server {
    listen 80;
    server_name offering.example.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    client_max_body_size 16M;
}
```

## Security Considerations

### Current Implementation
- Development server (not production-ready)
- No authentication
- No rate limiting
- File uploads in temp directory
- No persistent storage

### Production Recommendations
1. **Use production WSGI server** (Gunicorn, uWSGI)
2. **Add authentication** (OAuth, JWT)
3. **Implement rate limiting** (Flask-Limiter)
4. **Secure file uploads** (virus scanning, type validation)
5. **Use HTTPS** (Let's Encrypt)
6. **Database for persistence** (PostgreSQL, MongoDB)
7. **Session management** (secure cookies)
8. **Input sanitization** (prevent injection)

## Customization

### Change Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #your-color;
    --primary-hover: #your-hover-color;
}
```

### Add New Mode
1. Add button in `templates/index.html`
2. Add content section
3. Add handler in `static/js/app.js`
4. Add API endpoint in `app.py` if needed

### Modify Template
The PowerPoint template is loaded from:
```python
template_path = "templates/offer_template.pptx"
```

Change to support multiple templates:
```python
template = request.json.get('template', 'default')
template_path = f"templates/{template}_template.pptx"
```

## Troubleshooting

### Server won't start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Use different port
python app.py --port 8080  # (modify app.py to support this)
```

### CORS errors
```bash
# Install flask-cors
pip install flask-cors

# Already configured in app.py with CORS(app)
```

### File upload fails
- Check `MAX_CONTENT_LENGTH` setting
- Verify file format (.yaml, .yml, .json)
- Check temp directory permissions

### YAML parsing errors
- Verify js-yaml library loads (check browser console)
- Test with simple YAML first
- Use YAML validator online

## Future Enhancements

### Phase 1
- [ ] Multi-language support (EN, DE, FR)
- [ ] Dark mode toggle
- [ ] Save drafts locally (localStorage)
- [ ] Export to PDF option

### Phase 2
- [ ] User accounts & authentication
- [ ] Offer history & versioning
- [ ] Template gallery
- [ ] Real-time collaboration

### Phase 3
- [ ] API key management
- [ ] Webhook integrations
- [ ] Analytics dashboard
- [ ] Email sending

## Support

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Mobile Support
- iOS 14+
- Android 10+

## Examples

### Screenshot Workflow
1. Open http://localhost:5000
2. Select "Chat Extraction"
3. Paste offer description
4. Click "Daten Extrahieren"
5. Review in Preview section
6. Click "Preis Berechnen"
7. Click "PowerPoint Generieren"
8. Download file

### API Test with curl
```bash
# Extract
curl -X POST http://localhost:5000/api/extract \
  -H "Content-Type: application/json" \
  -d '{"text":"Angebot für Test, 3 Monate, 2 Dev à 800€"}'

# Generate (with full data)
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d @data/example.json \
  -o offer.pptx
```

---

**Built with care. Designed for elegance. Made for humans.** ✨
