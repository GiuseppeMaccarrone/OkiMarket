// src/components/ProductList.jsx
import ProductCard from './ProductCard';

// Assicurati di aggiungere onProductClick qui nelle parentesi graffe!
export default function ProductList({ products, onProductClick }) {
  return (
    <div style={styles.grid}>
      {products.map(product => (
        <ProductCard
          key={product.id}
          product={product}
          onProductClick={onProductClick} // <--- Fondamentale: passala qui!
        />
      ))}
    </div>
  );
}

const styles = {
  grid: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '20px',
    justifyContent: 'center'
  }
};