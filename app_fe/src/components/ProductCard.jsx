import React from 'react';
import { useSnackbar } from '../context/SnackbarContext';

// Icona SVG Carrello
const CartIcon = ({ size = 18, color = "white" }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke={color}
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <circle cx="9" cy="21" r="1"></circle>
    <circle cx="20" cy="21" r="1"></circle>
    <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
  </svg>
);

export default function ProductCard({ product, onProductClick }) {
  const showSnackbar = useSnackbar();
  const defaultImage = "/images/default-product.png";

  const imageUrl = (product.image_url && product.image_url.trim() !== "")
    ? `http://localhost:9000/products/${product.image_url}`
    : defaultImage;

  // Gestione aggiunta al carrello
  const addToCart = (e, product) => {
    // IMPORTANTE: ferma la propagazione del click alla card sottostante
    e.stopPropagation();

    const cartIds = JSON.parse(sessionStorage.getItem('cartIds') || '[]');
    cartIds.push(product.id);
    sessionStorage.setItem('cartIds', JSON.stringify(cartIds));

    window.dispatchEvent(new Event('cartUpdated'));
    showSnackbar(`${product.name} aggiunto al carrello!`);
  };

  return (
    <div
      style={styles.card}
      onClick={() => onProductClick(product.id)}
    >
      <div style={styles.imageContainer}>
        <img
          src={imageUrl}
          alt={product.name}
          style={styles.image}
          onError={(e) => { e.target.src = defaultImage; }}
        />
      </div>

      <div style={styles.info}>
        <h3 style={styles.title}>{product.name}</h3>

        <div style={styles.actionRow}>
          <p style={styles.price}>€{product.price}</p>

          <button
            style={styles.cartButton}
            onClick={(e) => addToCart(e, product)}
            title={`Aggiungi ${product.name} al carrello`}
          >
            <CartIcon color="white" />
          </button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  card: {
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '16px',
    marginLeft: '8px',
    marginRight: '8px',
    width: '200px',
    boxShadow: '0 2px 5px rgba(0,0,0,0.05)',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: 'white',
    overflow: 'hidden',
    cursor: 'pointer', // Fa capire che la card è un bottone
    transition: 'transform 0.1s ease', // Feedback al passaggio del mouse
  },
  imageContainer: {
    width: '100%',
    paddingTop: '100%',
    position: 'relative',
    backgroundColor: '#f9f9f9',
    borderRadius: '4px',
    marginBottom: '10px'
  },
  image: {
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    objectFit: 'contain'
  },
  info: { marginTop: '5px' },
  title: { fontSize: '16px', margin: '0 0 10px 0' },
  actionRow: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    borderTop: '1px solid #eee',
    paddingTop: '10px'
  },
  cartButton: {
    backgroundColor: '#FF9900',
    border: 'none',
    borderRadius: '4px',
    padding: '8px 12px',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  },
  price: { color: '#2c3e50', fontWeight: 'bold', margin: 0, fontSize: '18px' },
};