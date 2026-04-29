# OkiMarket - Prototipo E-commerce Full-Stack

OkiMarket è un prototipo avanzato di piattaforma e-commerce costruito con un'architettura a microservizi. Il progetto è focalizzato su prestazioni asincrone, integrità dei dati e automazione del workflow di sviluppo.

## Avvio Rapido (Zero Configuration)

Il progetto è completamente containerizzato tramite Docker. Non è necessaria alcuna configurazione manuale di database o storage locali.

1. **Clonare il repository**


2. **Configurare l'ambiente**: Creare un file `.env` nella radice del progetto partendo dall'esempio fornito:
   ```bash
   cp .env.example .env
   ```
    Assicurati di avere [Docker](https://docs.docker.com/) installato.


3. **Avvia i servizi**:
   ```bash
   docker-compose up --build
   ```

# Struttura del Progetto

```text
.
├── app_be/                 # Backend (FastAPI)
│   ├── routes/             # Endpoint API (es. product_routes.py)
│   ├── models/             # Modelli DB e Pydantic
│   ├── services/           # Logica pricipale BE
│   ├── tests/              # Suite di testing
│   └── alembic/            # Versionamento del database
│   ...
│   ...
├── app_fe/                 # Frontend (React)
│   └── src/
│       └── components/     # Componenti UI (es. ProductCard.jsx)
│   ...
│   ...
├── docker-compose.yaml     # Orchestrazione servizi
└── README.md               # Documentazione
```

## Frontend
- **Libreria**: React.js
- **Componentistica**: UI basata su componenti modulari (es. `ProductCard.jsx`)

## Backend
Il progetto è costruito seguendo standard rigorosi per garantire la massima stabilità:

- **Restrizioni dei Modelli**: Utilizziamo le definizioni dei modelli (Pydantic/SQLAlchemy) per imporre vincoli rigorosi sui dati in ingresso, prevenendo input invalidi prima ancora che raggiungano il database. L'uso di strutture tipizzate come `ProductSort` in `app_be/routes/product_routes.py` garantisce coerenza nei dati scambiati.
- **Gestione Migrazioni**: Grazie ad **Alembic**, ogni modifica allo schema del database è tracciata, versionata e testabile, eliminando i conflitti di schema tra ambienti diversi.
- **Testing**: La suite di test copre i casi critici del business logic. L'integrazione con CI/CD assicura che ogni commit mantenga intatta l'integrità del sistema.

### Infrastruttura
- **Containerizzazione**: Docker & Docker Compose