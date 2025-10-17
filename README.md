# Catalog Application - Backend

**Backend API REST per la gestione di cataloghi di accessori moda.** 

Include un media manager per il caricamento file e supporto per traduzioni dei nomi catalogo.

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
source venv/bin/activate
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

## Risorse Utili

### Documentazione Framework
- [Django](https://docs.djangoproject.com/) - Framework principale
- [Django REST Framework](https://www.django-rest-framework.org/) - API REST

### Media & Autenticazione
- [Django Filer](https://django-filer.readthedocs.io/) - Media manager
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/) - Autenticazione JWT

### UI & Admin
- [Django Jazzmin](https://django-jazzmin.readthedocs.io/) - Tema admin

---

## Autore

**Katia** - [GitHub](https://github.com/katiaITS)