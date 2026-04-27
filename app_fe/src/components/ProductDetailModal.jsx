import React, { useState, useEffect } from 'react';
import { getProductById, getCategoryById, deleteProduct } from '../services/api';
import { useSnackbar } from '../context/SnackbarContext';

export default function ProductDetailModal({
  productId,
  isOpen,
  onClose,
  onAddToCart,
  onEditClick,
  onDeleteSuccess
}) {
  const showSnackbar = useSnackbar();
  const [product, setProduct] = useState(null);
  const [category, setCategory] = useState(null);
  const [loading, setLoading] = useState(true);

  const MINIO_URL = "http://localhost:9000/products";

  useEffect(() => {
    if (isOpen && productId) {
      const fetchAllData = async () => {
        try {
          setLoading(true);
          const prodData = await getProductById(productId);
          setProduct(prodData);

          if (prodData.category_id) {
            const catData = await getCategoryById(prodData.category_id);
            setCategory(catData);
          }
        } catch (err) {
          console.error(err);
          showSnackbar("Errore nel recupero dati prodotto", true);
        } finally {
          setLoading(false);
        }
      };
      fetchAllData();
    } else {
      setProduct(null);
      setCategory(null);
    }
  }, [isOpen, productId]);

  if (!isOpen) return null;

  const formatDate = (dateStr) => {
    if (!dateStr) return "-";
    return new Date(dateStr).toLocaleDateString('it-IT', {
      day: '2-digit', month: 'long', year: 'numeric'
    });
  };

  const handleDelete = async () => {
    if (!window.confirm("Vuoi davvero eliminare questo prodotto? L'azione è irreversibile.")) return;
    try {
      await deleteProduct(product.id);
      showSnackbar("Prodotto eliminato correttamente");
      onDeleteSuccess(); // Ricarica la lista e chiude la modale
    } catch (err) {
      showSnackbar("Errore durante l'eliminazione", true);
    }
  };

  const handleAddToCartWithNotify = () => {
    onAddToCart(product);
    showSnackbar(`${product.name} aggiunto al carrello!`);
    // Opzionale: onClose(); se vuoi che si chiuda subito
  };

  return (
    <div style={styles.overlay} onClick={onClose}>
      <div style={styles.content} onClick={e => e.stopPropagation()}>
        <button style={styles.closeBtn} onClick={onClose}>✕</button>

        {loading ? (
          <div style={{ padding: '60px', textAlign: 'center' }}>
            <p style={{ color: '#666' }}>Caricamento dettagli...</p>
          </div>
        ) : product && (
          <div style={styles.container}>

            {/* Sinistra: Immagine */}
            <div style={styles.imageSection}>
              <img
                src={product.image_url ? `${MINIO_URL}/${product.image_url}` : "/images/default-product.png"}
                alt={product.name}
                style={styles.image}
                onError={(e) => { e.target.src = "/images/default-product.png"; }}
              />
            </div>

            {/* Destra: Info */}
            <div style={styles.infoSection}>
              <div style={styles.headerRow}>
                <small style={styles.productId}>ID Prodotto: {product.id}</small>
                <div style={styles.adminActions}>
                   <button onClick={() => onEditClick(product)} style={styles.editBtn}>✎ Modifica</button>
                   <button onClick={handleDelete} style={styles.delBtn}>🗑 Elimina</button>
                </div>
              </div>

              <h1 style={styles.title}>{product.name}</h1>

              <p style={styles.categoryLabel}>
                Categoria: <span style={styles.categoryName}>{category ? category.name : 'N/A'}</span>
              </p>

              <hr style={styles.divider} />

              <p style={styles.price}>€{product.price.toFixed(2)}</p>

              <div style={styles.tagsContainer}>
                {product.tags && product.tags.length > 0 ? (
                  product.tags.map((tag, i) => (
                    <span key={i} style={styles.tag}>#{tag}</span>
                  ))
                ) : <small style={{color: '#999'}}>Nessun tag</small>}
              </div>

              <div style={styles.metadata}>
                <p>Inserito il: <strong>{formatDate(product.created_at)}</strong></p>
              </div>

              <button
                style={styles.cartBtn}
                onClick={handleAddToCartWithNotify}
              >
                Aggiungi al carrello
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  overlay: { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.7)', zIndex: 4000, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: "'Roboto', sans-serif" },
  content: { backgroundColor: 'white', borderRadius: '12px', width: '850px', maxWidth: '95%', position: 'relative', overflow: 'hidden', boxShadow: '0 15px 50px rgba(0,0,0,0.3)' },
  closeBtn: { position: 'absolute', top: '15px', right: '15px', border: 'none', background: '#f0f0f0', borderRadius: '50%', width: '35px', height: '35px', cursor: 'pointer', zIndex: 10, fontWeight: 'bold' },
  container: { display: 'flex', flexDirection: 'row', gap: '40px', padding: '40px' },

  imageSection: { flex: '0 0 45%', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#fff', border: '1px solid #eee', borderRadius: '8px', padding: '20px' },
  image: { maxWidth: '100%', maxHeight: '450px', objectFit: 'contain' },

  infoSection: { flex: 1, display: 'flex', flexDirection: 'column' },
  headerRow: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '5px' },
  productId: { color: '#888', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.5px' },
  adminActions: { display: 'flex', gap: '10px' },
  editBtn: { background: '#f0f7f8', border: '1px solid #007185', color: '#007185', borderRadius: '4px', cursor: 'pointer', padding: '4px 10px', fontSize: '12px', fontWeight: 'bold' },
  delBtn: { background: '#fcf0f0', border: '1px solid #CC0C39', color: '#CC0C39', borderRadius: '4px', cursor: 'pointer', padding: '4px 10px', fontSize: '12px', fontWeight: 'bold' },

  title: { fontSize: '32px', margin: '0 0 15px 0', color: '#111', lineHeight: '1.2' },
  categoryLabel: { fontSize: '16px', color: '#555' },
  categoryName: { color: '#007185', fontWeight: 'bold' },
  divider: { border: '0', borderTop: '1px solid #eee', margin: '20px 0' },
  price: { fontSize: '36px', color: '#B12704', margin: '0 0 20px 0', fontWeight: '500' },
  tagsContainer: { display: 'flex', gap: '8px', marginBottom: '25px', flexWrap: 'wrap' },
  tag: { backgroundColor: '#e7f4f5', padding: '6px 14px', borderRadius: '4px', fontSize: '13px', color: '#007185', fontWeight: '500', border: '1px solid #007185' },
  metadata: { marginBottom: '30px', fontSize: '14px', color: '#555' },
  cartBtn: { backgroundColor: '#FF9900', border: '1px solid #a88734', padding: '16px', borderRadius: '8px', fontWeight: 'bold', cursor: 'pointer', fontSize: '18px', boxShadow: '0 2px 5px rgba(0,0,0,0.1)', transition: 'background 0.2s' }
};