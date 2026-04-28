import Navbar from './components/Navbar.jsx';
import ProductList from './components/ProductList.jsx';
import React, { useState, useEffect } from 'react';
import CartSidebar from './components/CartSidebar';
import { getProducts } from './services/api';
import CategoryModal from './components/CategoryModal';
import ProductModal from './components/ProductModal';
import { SnackbarProvider } from './context/SnackbarContext';
import CategoryManagerModal from './components/CategoryManagerModal';
import ProductDetailModal from './components/ProductDetailModal';

export default function App() {
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Stato per paginazione
  const [page, setPage] = useState(0);
  const [currentFilters, setCurrentFilters] = useState({});
  const LIMIT = 20;

  // Modali
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showProductModal, setShowProductModal] = useState(false);
  const [showCategoryModal, setShowCategoryModal] = useState(false);
  const [showCategoryManager, setShowCategoryManager] = useState(false);

  const [selectedProductId, setSelectedProductId] = useState(null);

  const [productToEdit, setProductToEdit] = useState(null);

  // Caricamento prodotti aggiornato con skip/limit
  const loadProducts = async (filters = null) => {
    try {
      setLoading(true);

      let filtersToUse = currentFilters;
      if (filters !== null) {
        filtersToUse = filters;
        setCurrentFilters(filters);
        setPage(0);
      }

      const params = {
        ...filtersToUse,
        skip: (filters ? 0 : page) * LIMIT,
        limit: LIMIT
      };
      const data = await getProducts(params);
      setProducts(data);
    } catch (error) {
      console.error("Errore nel caricamento prodotti:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenEdit = (product) => {
    setSelectedProductId(null); // Chiudi dettagli
    setProductToEdit(product);  // Apri modifica
  };

  const handleAddToCart = (product) => {
    const cartIds = JSON.parse(sessionStorage.getItem('cartIds') || '[]');
    cartIds.push(product.id);
    sessionStorage.setItem('cartIds', JSON.stringify(cartIds));
    window.dispatchEvent(new Event('cartUpdated'));
    // Qui servirebbe useSnackbar, ma siccome App è fuori dal provider,
    // la notifica la gestiranno i componenti figli o la ProductCard stessa.
  };

  useEffect(() => {
    loadProducts();
  }, [page]);

  return (
    <SnackbarProvider>
      <div style={{ fontFamily: "'Roboto', sans-serif", margin: 0, minHeight: '100vh', position: 'relative' }}>
        <Navbar
          onCartClick={() => setIsCartOpen(true)}
          onSearch={loadProducts}
          onManageCategories={() => setShowCategoryManager(true)}
        />

        <CartSidebar
          isOpen={isCartOpen}
          onClose={() => setIsCartOpen(false)}
        />

        <main style={{ padding: '20px', paddingBottom: '80px' }}>
          <h2>Prodotti in evidenza</h2>

          {loading ? (
            <div style={{ textAlign: 'center', marginTop: '50px' }}>
              <p>Caricamento prodotti in corso...</p>
            </div>
          ) : (
            products.length > 0 ? (
              <ProductList
                products={products}
                onProductClick={(id) => setSelectedProductId(id)}
              />
            ) : (
              <p style={{ textAlign: 'center' }}>Nessun prodotto trovato.</p>
            )
          )}

          {/* CONTROLLI PAGINAZIONE */}
          <div style={styles.pagination}>
            <button
              disabled={page === 0}
              onClick={() => setPage(page - 1)}
              style={styles.pageBtn}
            >
              Precedente
            </button>
            <span>Pagina {page + 1}</span>
            <button
              onClick={() => setPage(page + 1)}
              style={styles.pageBtn}
            >
              Successiva
            </button>
          </div>
        </main>

        {/* BOTTONE "+" (FAB) */}
        <div
          style={styles.fabContainer}
          onMouseEnter={() => setIsMenuOpen(true)}
          onMouseLeave={() => setIsMenuOpen(false)}
        >
          <div style={isMenuOpen ? styles.fabPillOpen : styles.fabPillClosed}>
            <div style={styles.contentWrapper}>
              <div style={{...styles.plusIcon, opacity: isMenuOpen ? 0 : 1}}>+</div>
              <div style={{...styles.menuTextContent, opacity: isMenuOpen ? 1 : 0}}>
                <button style={styles.pillButton} onClick={() => setShowProductModal(true)}>PRODOTTO</button>
                <div style={styles.divider}></div>
                <button style={styles.pillButton} onClick={() => setShowCategoryModal(true)}>CATEGORIA</button>
              </div>
            </div>
          </div>
        </div>

        {showCategoryModal && (
          <CategoryModal
            isOpen={showCategoryModal}
            onClose={() => setShowCategoryModal(false)}
          />
        )}

        {showProductModal && (
          <ProductModal
            isOpen={showProductModal}
            onClose={() => setShowProductModal(false)}
          />
        )}
      </div>
    <CategoryManagerModal
      isOpen={showCategoryManager}
      onClose={() => setShowCategoryManager(false)}
    />

    <ProductDetailModal
      productId={selectedProductId}
      isOpen={!!selectedProductId}
      onClose={() => setSelectedProductId(null)}
      onAddToCart={handleAddToCart}
      onEditClick={handleOpenEdit}
      onDeleteSuccess={() => { setSelectedProductId(null); loadProducts(); }}
    />

    <ProductModal
      isOpen={!!productToEdit}
      initialData={productToEdit}
      onClose={() => setProductToEdit(null)}
      onRefresh={loadProducts}
    />
    </SnackbarProvider>
  );
}

const styles = {
  pagination: { display: 'flex', justifyContent: 'center', gap: '15px', marginTop: '40px', alignItems: 'center' },
  pageBtn: { padding: '8px 16px', backgroundColor: '#fff', border: '1px solid #d5d9d9', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' },
  fabContainer: { position: 'fixed', bottom: '30px', right: '30px', zIndex: 1000, height: '60px', display: 'flex', alignItems: 'center' },
  fabPillClosed: { width: '60px', height: '60px', borderRadius: '30px', backgroundColor: '#FF9900', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 4px 10px rgba(0,0,0,0.3)', overflow: 'hidden', transition: 'all 0.4s' },
  fabPillOpen: { width: '220px', height: '60px', borderRadius: '30px', backgroundColor: '#FF9900', display: 'flex', alignItems: 'center', padding: '0 20px', boxShadow: '0 4px 10px rgba(0,0,0,0.3)', overflow: 'hidden', transition: 'all 0.4s' },
  contentWrapper: { display: 'flex', alignItems: 'center', width: '100%', position: 'relative' },
  plusIcon: { color: 'white', fontSize: '30px', fontWeight: 'bold', position: 'absolute', left: '22.5px', transition: 'opacity 0.2s' },
  menuTextContent: { display: 'flex', alignItems: 'center', gap: '15px', whiteSpace: 'nowrap', transition: 'opacity 0.3s' },
  pillButton: { background: 'transparent', border: 'none', color: 'white', fontWeight: 'bold', cursor: 'pointer', fontSize: '14px' },
  divider: { width: '1px', height: '20px', backgroundColor: 'rgba(255,255,255,0.5)' }
};