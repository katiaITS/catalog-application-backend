# Catalog Application - Backend

**Backend API REST per la gestione del catalogo di un azienda in campo moda** 

Questo progetto permette ai dipendenti dell'azienda di gestire cataloghi organizzati in categorie, con supporto per caricamento file tramite media manager integrato. Include un pannello di amministrazione con permessi differenziati per gestire cataloghi, categorie e file multimediali.

---

## Funzionalità Principali

### Gestione Cataloghi e Categorie
- Operazioni CRUD complete (creazione, lettura, modifica, eliminazione)
- Supporto traduzioni manuali per nomi (IT, EN, FR, ES)
- Associazione di file alle categorie o ai cataloghi
- Struttura gerarchica a categorie e sottocategorie

### Gestione File e Media
- Caricamento e eliminazione file tramite media manager integrato (Filer)
- Spostamento file tra cartelle
- Importazione massiva di file multipli
- Ordinamento alfabetico intelligente (A1 < A2 < A10)

### Gestione Utenti
- Sistema di ruoli e permessi differenziati (Superuser, Staff, User)
- Creazione e gestione account utenti
- Controllo accessi basato su ruolo

### Pannello Admin Personalizzato
- Interfaccia moderna e responsive (Jazzmin Theme)
- Inline editing per gestione rapida
- Filtri avanzati per catalogo, categoria, tipo file

---

## Tecnologie

- **Django 5.2.7** - Framework web Python
- **Django REST Framework** - Gestione API REST
- **djangorestframework-simplejwt** - Autenticazione tramite token JWT
- **Django Filer 3.3.2** - Media manager avanzato
- **Pillow** - Elaborazione immagini
- **django-jazzmin** - Tema admin moderno

---

## Installazione

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
source venv\Scripts\activate
```

### 3. Installa Dipendenze
```bash
pip install -r requirements.txt
```

### 4. Configura Variabili d'Ambiente
```bash
# Windows
copy .env.example .env

# Linux/Mac
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

### 7. Avvia Server di Sviluppo
```bash
python manage.py runserver
```

Il server sarà disponibile su: `http://localhost:8000`  
Admin panel: `http://localhost:8000/admin/`

---

## Futuri Sviluppi

### Versione 1

**Gestione Prodotti Avanzata**
- Associazione di codici prodotto multipli a ogni immagine con descrizioni
- Ricerca avanzata per codice prodotto, nome immagine, categoria o parole chiave

**Autenticazione Cliente**
- API di registrazione cliente con profili personalizzati

**Mobile**
- Sistema di autenticazione JWT per app mobile
- Download immagini ottimizzato per mobile

**Funzionalità Utente**
- Sistema preferiti per salvare prodotti

**Automazione**
- **Traduzione automatica multilingua**: generazione automatica traduzioni nomi cataloghi/categorie (attualmente manuale)
- **Sincronizzazione Filer → Modelli**: creazione automatica oggetti Cartelle quando si carica file su media manager con associazione intelligente a cataloghi/categorie

### Versione 2
**Intelligenza Artificiale**
- Riconoscimento automatico codici prodotto dalle immagini tramite OCR/AI
- Associazione automatica codice → immagine

**Gestione Listini Prezzi**
- Import automatico da file esterni (CSV/Excel/PDF)
- Modello Listino con codice articolo, descrizione, fasce prezzo
- Associazione automatica immagini ↔ listini tramite codice articolo
- API per visualizzazione listini nell'app mobile

**Analytics**
- Tracking visualizzazioni e ricerche più frequenti
- Dashboard statistiche per amministratori

**Mobile**
- Sistema di notifica per aggiornamenti automatici verso app mobile

---

## Schema Database

### Modelli Principali

**Catalogo**
- Campi multilingua (nome_it, nome_en, nome_fr, nome_es)
- Slug univoco per URL SEO-friendly
- Immagine copertina
- Relazione **1:N** con Categoria
- Relazione **M:N** con Cartelle (file root del catalogo)

**Categoria**
- Struttura gerarchica (parent/child) per sottocategorie
- Campi multilingua
- Relazione **N:1** con Catalogo
- Relazione **M:N** con Cartelle (file categorizzati)

**Cartelle** (File Manager)
- Supporto upload diretto o selezione da Django Filer
- Rilevamento automatico tipo file (PDF, immagine, video, documento)
- Ordinamento intelligente alfanumerico (A1 < A2 < A10)
- Relazioni **M:N** con Catalogo e Categoria tramite tabelle ponte
- Tracking creazione/modifica utente

**ProfiloUtente**
- Estensione modello User Django
- Relazione **1:1** con User
- Campi personalizzabili (es: nome_azienda)

### Tabelle Ponte (Many-to-Many)
- **CatalogoCartella**: associa file al catalogo root con ordinamento
- **CategoriaCartella**: associa file alle categorie con ordinamento

---

## Risorse Utili

### Documentazione Framework
- [Django](https://docs.djangoproject.com/) - Framework principale
- [Django REST Framework](https://www.django-rest-framework.org/) - API REST
- [Python Decouple](https://pypi.org/project/python-decouple/) - Gestione variabili ambiente

### Media & Autenticazione
- [Django Filer](https://django-filer.readthedocs.io/) - Media manager
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/) - Autenticazione JWT

### UI & Admin
- [Django Jazzmin](https://django-jazzmin.readthedocs.io/) - Tema admin

---

## Autore

**Katia** - [GitHub](https://github.com/katiaITS)
