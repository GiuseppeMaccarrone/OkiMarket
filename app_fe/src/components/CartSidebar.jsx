import { useEffect, useState } from 'react';
import { getProductById } from '../services/api';

// Funzione helper per le immagini (spostabile in un file utils se preferisci)
const getImageUrl = (imageName) => {
  const MINIO_PUBLIC_URL = "http://localhost:9000/products";
  const defaultImage = "/images/default-product.png";

  if (!imageName || imageName.trim() === "") return defaultImage;
  if (imageName.startsWith('http')) return imageName;
  return `${MINIO_PUBLIC_URL}/${imageName}`;
};

export default function CartSidebar({ isOpen, onClose }) {
  const [cartItems, setCartItems] = useState([]);

  useEffect(() => {
    if (isOpen) {
      loadCartDetails();
    }
    window.addEventListener('cartUpdated', loadCartDetails);
    return () => window.removeEventListener('cartUpdated', loadCartDetails);
  }, [isOpen]);

  const loadCartDetails = async () => {
    const savedIds = JSON.parse(sessionStorage.getItem('cartIds') || '[]');
    if (savedIds.length === 0) {
      setCartItems([]);
      return;
    }

    try {
      const promises = savedIds.map(id => getProductById(id));
      const products = await Promise.all(promises);
      setCartItems(products);
    } catch (error) {
      console.error("Errore nel recupero prodotti carrello:", error);
    }
  };

  const removeItem = (idToRemove) => {
    const savedIds = JSON.parse(sessionStorage.getItem('cartIds') || '[]');
    const index = savedIds.indexOf(idToRemove);
    if (index > -1) {
      savedIds.splice(index, 1);
    }
    sessionStorage.setItem('cartIds', JSON.stringify(savedIds));
    window.dispatchEvent(new Event('cartUpdated'));
  };

  const total = cartItems.reduce((sum, item) => sum + item.price, 0);

  if (!isOpen) return null;

  return (
    <div style={styles.sidebar}>
      <div style={styles.header}>
        <h2 style={{ margin: 0 }}>Il tuo Carrello</h2>
        <button onClick={onClose} style={styles.closeBtn}>✕</button>
      </div>

      <div style={styles.items}>
        {cartItems.map((item, index) => (
          <div key={`${item.id}-${index}`} style={styles.miniCard}>
            <img
              src={getImageUrl(item.image_url)}
              style={styles.miniImg}
              alt={item.name}
              onError={(e) => { e.target.src = "/images/default-product.png"; }}
            />
            <div style={styles.miniInfo}>
              <p style={{margin:0}}>{item.name}</p>
              <p style={{margin:0, fontWeight:'bold'}}>€{item.price}</p>
            </div>
            <button onClick={() => removeItem(item.id)} style={styles.removeBtn}>Rim.</button>
          </div>
        ))}
      </div>

      <div style={styles.total}>
        <h3>Totale: €{total.toFixed(2)}</h3>
        <button style={styles.checkoutBtn}>Procedi al pagamento</button>
      </div>
    </div>
  );
}

const styles = {
  sidebar: {
    position: 'fixed', right: 0, top: 0, height: '100%', width: '300px',
    backgroundColor: 'white', zIndex: 2000, boxShadow: '-2px 0 5px rgba(0,0,0,0.2)',
    padding: '20px', display: 'flex', flexDirection: 'column', boxSizing: 'border-box'
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px'
  },
  closeBtn: {
    cursor: 'pointer', border: 'none', background: '#eee', borderRadius: '50%',
    width: '30px', height: '30px', fontWeight: 'bold', display: 'flex',
    alignItems: 'center', justifyContent: 'center'
  },
  items: { flex: 1, overflowY: 'auto', marginBottom: '10px' },
  total: {
    borderTop: '2px solid #232f3e',
    paddingTop: '20px',
    paddingBottom: '20px',
    backgroundColor: 'white'
  },
  miniCard: { display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '15px', borderBottom: '1px solid #eee', paddingBottom: '10px' },
  miniImg: { width: '50px', height: '50px', objectFit: 'cover', borderRadius: '4px' },
  miniInfo: { flexGrow: 1 },
  removeBtn: { fontSize: '12px', color: 'red', cursor: 'pointer', background: 'none', border: 'none' },
  checkoutBtn: { width: '100%', padding: '10px', backgroundColor: '#FF9900', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }
};