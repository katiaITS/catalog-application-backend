# 📚 GIMA Application Backend

Backend API per la gestione di cataloghi multilingua con Django REST Framework.

## 🚀 Quick Start

### 1. Clona il Repository
```bash
git clone https://github.com/katiaITS/catalog-application-backend.git
cd catalog-application-backend
```

### 2. Crea Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Installa Dipendenze
```bash
pip install -r requirements.txt
```

### 4. Configura Variabili d'Ambiente
```bash
# Copia il template
cp .env.example .env

# Modifica .env con i tuoi valori
# IMPORTANTE: Genera una nuova SECRET_KEY per produzione!
```

### 5. Applica Migrations
```bash
python manage.py migrate
```

### 6. Crea Superuser
```bash
python manage.py createsuperuser
```

### 7. Avvia Server
```bash
python manage.py runserver
```

Il server sarà disponibile su: `http://localhost:8000`

---

## 🔧 Configurazione

### Variabili d'Ambiente (.env)

| Variabile | Descrizione | Default | Obbligatorio |
|-----------|-------------|---------|--------------|
| `SECRET_KEY` | Chiave segreta Django | - | ✅ |
| `DEBUG` | Modalità debug | `False` | ❌ |
| `ALLOWED_HOSTS` | Host permessi | `localhost,127.0.0.1` | ❌ |
| `CORS_ALLOW_ALL_ORIGINS` | Permetti tutti CORS | `False` | ❌ |
| `CORS_ALLOWED_ORIGINS` | Domini CORS specifici | - | ❌ |
| `JWT_ACCESS_TOKEN_MINUTES` | Durata access token (minuti) | `60` | ❌ |
| `JWT_REFRESH_TOKEN_DAYS` | Durata refresh token (giorni) | `7` | ❌ |

### Generare una Nuova SECRET_KEY

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📡 API Endpoints

### Autenticazione (JWT)

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Ottieni token (access + refresh) |
| POST | `/api/auth/refresh/` | Rinnova access token |
| POST | `/api/auth/verify/` | Verifica validità token |

**Esempio Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

**Risposta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Cataloghi

| Metodo | Endpoint | Descrizione | Auth |
|--------|----------|-------------|------|
| GET | `/api/cataloghi/` | Lista cataloghi | ✅ |
| POST | `/api/cataloghi/` | Crea catalogo | ✅ |
| GET | `/api/cataloghi/{id}/` | Dettaglio catalogo | ✅ |
| PUT | `/api/cataloghi/{id}/` | Modifica completa | ✅ |
| PATCH | `/api/cataloghi/{id}/` | Modifica parziale | ✅ |
| DELETE | `/api/cataloghi/{id}/` | Elimina catalogo | ✅ |

### Categorie

| Metodo | Endpoint | Descrizione | Auth |
|--------|----------|-------------|------|
| GET | `/api/categorie/` | Lista categorie | ✅ |
| POST | `/api/categorie/` | Crea categoria | ✅ |
| GET | `/api/categorie/{id}/` | Dettaglio categoria | ✅ |
| PUT | `/api/categorie/{id}/` | Modifica completa | ✅ |
| PATCH | `/api/categorie/{id}/` | Modifica parziale | ✅ |
| DELETE | `/api/categorie/{id}/` | Elimina categoria | ✅ |

### Cartelle (Files)

| Metodo | Endpoint | Descrizione | Auth |
|--------|----------|-------------|------|
| GET | `/api/cartelle/` | Lista cartelle | ✅ |
| POST | `/api/cartelle/` | Crea cartella | ✅ |
| GET | `/api/cartelle/{id}/` | Dettaglio cartella | ✅ |
| PUT | `/api/cartelle/{id}/` | Modifica completa | ✅ |
| PATCH | `/api/cartelle/{id}/` | Modifica parziale | ✅ |
| DELETE | `/api/cartelle/{id}/` | Elimina cartella | ✅ |

**Usare il Token:**
```bash
curl -X GET http://localhost:8000/api/cataloghi/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🗂️ Struttura Progetto

```
gima-application-backend/
├── catalogo/              # App principale
│   ├── models.py         # Modelli DB
│   ├── serializers.py    # Serializer DRF
│   ├── views.py          # ViewSets API
│   ├── admin.py          # Configurazione admin
│   └── urls.py           # URL routing
├── utenti/               # App utenti
│   ├── models.py         # ProfiloUtente
│   └── admin.py
├── config/               # Configurazione progetto
│   ├── settings.py       # Settings Django
│   ├── urls.py           # URL root
│   └── wsgi.py
├── media/                # File caricati
├── templates/            # Template HTML
├── .env                  # Variabili ambiente (NON committare!)
├── .env.example          # Template variabili
├── requirements.txt      # Dipendenze Python
├── manage.py            # CLI Django
└── db.sqlite3           # Database SQLite
```

---

## 🛠️ Stack Tecnologico

- **Framework:** Django 5.2.7
- **API:** Django REST Framework
- **Auth:** Simple JWT
- **Media:** Django Filer
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **CORS:** django-cors-headers
- **Config:** python-decouple

---

## 📦 Funzionalità

### Cataloghi Multilingua
- Supporto 4 lingue: IT, EN, FR, ES
- Slug automatici per URL SEO-friendly
- Immagini copertina
- Attivazione/disattivazione

### Categorie Gerarchiche
- Struttura ad albero (parent/child)
- Associazione a cataloghi
- Percorsi completi multilingua

### Gestione File
- Upload diretto o via Django Filer
- Relazioni many-to-many con cataloghi/categorie
- Ordinamento intelligente
- Thumbnail automatici

### Sicurezza
- Autenticazione JWT
- Permessi granulari
- CORS configurabile
- Tracciamento modifiche (created_by, updated_by)

---

## 🔐 Sicurezza

### ⚠️ IMPORTANTE per Produzione

1. **Genera nuova SECRET_KEY**
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **Disabilita DEBUG**
   ```bash
   DEBUG=False
   ```

3. **Configura ALLOWED_HOSTS**
   ```bash
   ALLOWED_HOSTS=tuodominio.com,www.tuodominio.com
   ```

4. **Configura CORS**
   ```bash
   CORS_ALLOW_ALL_ORIGINS=False
   CORS_ALLOWED_ORIGINS=https://tuofrontend.com
   ```

5. **Usa database PostgreSQL**
   ```bash
   pip install psycopg2-binary
   # Configura DATABASE_URL in .env
   ```

---

## 🧪 Testing

```bash
# Esegui tutti i test
python manage.py test

# Test per app specifica
python manage.py test catalogo

# Test con coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## 📝 Admin Panel

Accedi all'admin Django: `http://localhost:8000/admin/`

**Funzionalità Admin:**
- Gestione cataloghi con inline cartelle
- Gestione categorie con relazioni
- Upload multiplo file da Filer
- Filtri e ricerca avanzata
- Ordinamento drag & drop

---

## 🤝 Contribuire

1. Fork del progetto
2. Crea branch feature (`git checkout -b feature/nome-feature`)
3. Commit modifiche (`git commit -m 'Add: nuova feature'`)
4. Push branch (`git push origin feature/nome-feature`)
5. Apri Pull Request

---

## 📄 Licenza

[Specifica la tua licenza]

---

## 👥 Autori

- **Katia** - [katiaITS](https://github.com/katiaITS)

---

## 📞 Supporto

Per domande o problemi, apri una [issue](https://github.com/katiaITS/catalog-application-backend/issues).
