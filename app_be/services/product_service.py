
from models.product import ProductModelAlchemy, ProductCreate, Product, ProductSortBy, ProductQueryParams
from sqlalchemy import select, desc, asc, delete
from sqlalchemy.exc import IntegrityError
from config.database import AsyncSessionLocal
from models.category import CategoryModelAlchemy


class ProductService():

    async def create_product(self, product_data: ProductCreate):
        async with AsyncSessionLocal() as session:
            try:
                # 1. CONTROLLO: La categoria esiste?
                category_stmt = select(CategoryModelAlchemy).where(CategoryModelAlchemy.id == product_data.category_id)
                category_result = await session.execute(category_stmt)
                category = category_result.scalar_one_or_none()

                if not category:
                    return 404, {"error": f"Categoria con ID {product_data.category_id} non trovata."}

                # 2. Crea l'oggetto ORM
                new_product = ProductModelAlchemy(**product_data.model_dump())

                # 3. Aggiungi al db
                session.add(new_product)
                await session.commit()
                await session.refresh(new_product)

                # 4. Restituisci il dizionario pulito
                product_model = Product.model_validate(new_product)
                return 201, product_model.model_dump(mode='json')

            except IntegrityError as e:
                # Questo cattura errori di vincoli (es. FK fallita all'ultimo secondo)
                await session.rollback()
                return 400, {"error": "Errore di integrità del database (chiave esterna non valida)."}
            except Exception as e:
                await session.rollback()
                return 500, {"error": str(e)}

    async def update_product(self, product_id: int, product_data: ProductCreate):
        id = int(product_id)
        async with AsyncSessionLocal() as session:
            try:
                # 1. Recupera l'oggetto esistente dal DB
                result = await session.execute(
                    select(ProductModelAlchemy).filter(ProductModelAlchemy.id == id)
                )
                product_to_update = result.scalar_one_or_none()

                if not product_to_update:
                    return 404, {"error": "Prodotto non trovato"}

                # 2. Aggiorna i campi con i nuovi dati
                for key, value in product_data.model_dump().items():
                    setattr(product_to_update, key, value)

                # 3. Commit per salvare le modifiche
                await session.commit()
                await session.refresh(product_to_update)

                product_model = Product.model_validate(product_to_update)
                return 200, product_model.model_dump(mode='json')

            except Exception as e:
                await session.rollback()
                return 500, {"error": str(e)}

    async def get_by_id(self, product_id: int):
        id = int(product_id)
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ProductModelAlchemy).filter(ProductModelAlchemy.id == id)
            )
            product = result.scalar_one_or_none()

            if not product:
                return 404, {"error": "Prodotto non trovato"}

            product_model = Product.model_validate(product)
            return 200, product_model.model_dump(mode='json')

    async def delete(self, product_id: int):
        id = int(product_id)
        async with AsyncSessionLocal() as session:
            try:
                # 1. Verifica esistenza
                result = await session.execute(
                    select(ProductModelAlchemy).filter(ProductModelAlchemy.id == id)
                )
                product = result.scalar_one_or_none()

                if not product:
                    return 404, {"error": "Prodotto non trovato"}

                # 2. Elimina
                await session.execute(
                    delete(ProductModelAlchemy).filter(ProductModelAlchemy.id == id)
                )
                await session.commit()

                return 200, {"message": "Prodotto eliminato con successo"}
            except Exception as e:
                await session.rollback()
                return 500, {"error": str(e)}

    async def list(self, params: ProductQueryParams):
        async with AsyncSessionLocal() as session:
            # 1. Inizia con la query base
            query = select(ProductModelAlchemy)

            # 2. Applica i filtri dinamicamente
            if params.search:
                query = query.filter(ProductModelAlchemy.name.ilike(f"%{params.search}%"))

            if params.category_id:
                query = query.filter(ProductModelAlchemy.category_id == params.category_id)

            if params.min_price is not None:
                query = query.filter(ProductModelAlchemy.price >= params.min_price)

            if params.max_price is not None:
                query = query.filter(ProductModelAlchemy.price <= params.max_price)

            # 3. Applica l'ordinamento
            if params.sort_by == ProductSortBy.PRICE_ASC:
                query = query.order_by(asc(ProductModelAlchemy.price))
            elif params.sort_by == ProductSortBy.PRICE_DESC:
                query = query.order_by(desc(ProductModelAlchemy.price))
            elif params.sort_by == ProductSortBy.CREATED_AT_ASC:
                query = query.order_by(asc(ProductModelAlchemy.created_at))
            else:  # Default CREATED_AT_DESC
                query = query.order_by(desc(ProductModelAlchemy.created_at))

            # 4. Applica paginazione
            query = query.offset(params.skip).limit(params.limit)

            # 5. Esegui
            result = await session.execute(query)
            products = result.scalars().all()

            return 200, [Product.model_validate(p).model_dump(mode='json') for p in products]
