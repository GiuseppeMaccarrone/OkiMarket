import ProductCard from './ProductCard';

export default function ProductList({ products }) {
  return (
    <div style={styles.grid}>
      {products.map(product => <ProductCard key={product.id} product={product} />)}
    </div>
  );
}

const styles = {
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '45px', padding: '20px' }
};