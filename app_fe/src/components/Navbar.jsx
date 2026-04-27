import React, { useState, useEffect } from 'react';
import { getCategories } from '../services/api';

// Icona minimalista a imbuto (Funnel)
const FunnelIcon = ({ size = 20, color = "white" }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color}
       strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
  </svg>
);

const CartIcon = ({ size = 24, color = "white" }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color}
       strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="9" cy="21" r="1"></circle>
    <circle cx="20" cy="21" r="1"></circle>
    <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
  </svg>
);

export default function Navbar({ onCartClick, onSearch }) {
  const [isFilterOpen, setIsFilterOpen] = useState(false);

  // Stato per le categorie
  const [categories, setCategories] = useState([]);

  // Stati per i filtri
  const [search, setSearch] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [sort, setSort] = useState("created_at_desc");

  const [category, setCategory] = useState("");

  const sortOptions = [
    { label: "Prezzo decrescente", value: "price_desc" },
    { label: "Prezzo crescente", value: "price_asc" },
    { label: "Più recenti", value: "created_at_desc" },
    { label: "Più vecchi", value: "created_at_asc" }
  ];

  // Caricamento categorie all'avvio
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const data = await getCategories();
        setCategories(data);
      } catch (err) {
        console.error("Errore caricamento categorie:", err);
      }
    };
    fetchCategories();
  }, []);

  const handleSearch = () => {
    // Prepariamo un oggetto con i filtri
    const filters = { search, minPrice, maxPrice, sort };

    // Aggiungiamo category_id solo se è presente e non è una stringa vuota
    if (category && category !== "") {
      filters.category_id = parseInt(category);
    }

    onSearch(filters);
    setIsFilterOpen(false);
  };

  return (
    <nav style={styles.navbar}>
      <h1 style={styles.logo}>OkiMarket</h1>

      <div style={styles.searchContainer}>
        <input
          style={styles.searchInput}
          placeholder="Cerca nel catalogo..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <button style={styles.searchButton} onClick={handleSearch}>Cerca</button>

        <div style={styles.filterWrapper}>
          <button
            style={styles.filterIconButton}
            onClick={() => setIsFilterOpen(!isFilterOpen)}
            title="Filtri avanzati"
          >
            <FunnelIcon color="white" size={24} />
          </button>

          {isFilterOpen && (
            <div style={styles.filterPopover}>
              <div style={styles.popoverArrow}></div>

              <div style={styles.filterSection}>
                <label style={styles.sectionTitle}>PREZZO</label>
                <div style={styles.priceInputGroup}>
                  <input type="number" placeholder="MIN" style={styles.priceInputMin} value={minPrice} onChange={(e) => setMinPrice(e.target.value)} />
                  <input type="number" placeholder="MAX" style={styles.priceInputMax} value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)} />
                </div>
              </div>

              <div style={styles.filterSection}>
                <label style={styles.sectionTitle}>CATEGORIA</label>
                <select
                  style={styles.categorySelect}
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                >
                  <option value="">Tutte le categorie</option>
                  {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>
                      {cat.name}
                    </option>
                  ))}
                </select>
              </div>

              <div style={styles.filterSection}>
                <label style={styles.sectionTitle}>ORDINA PER</label>
                <select style={styles.categorySelect} value={sort} onChange={(e) => setSort(e.target.value)}>
                  {sortOptions.map(opt => (
                    <option key={opt.value} value={opt.value}>{opt.label}</option>
                  ))}
                </select>
              </div>

              <button style={styles.searchButton} onClick={handleSearch}>Applica Filtri</button>
            </div>
          )}
        </div>
      </div>

      <div style={styles.rightActions}>
        <button style={styles.cartIconButton} onClick={onCartClick}>
          <CartIcon color="white" size={24} />
        </button>
      </div>
    </nav>
  );
}

const styles = {
  navbar: {
    backgroundColor: '#232f3e', padding: '10px 20px', display: 'flex',
    alignItems: 'center', justifyContent: 'flex-start', gap: '30px',
    fontFamily: "'Roboto', sans-serif", width: '100%', boxSizing: 'border-box',
  },
  logo: { color: 'white', margin: 0, fontSize: '24px', whiteSpace: 'nowrap' },
  searchContainer: { display: 'flex', flex: '0 0 40%', minWidth: '300px', alignItems: 'center' },
  searchInput: { padding: '8px', flexGrow: 1, border: 'none', borderRadius: '4px 0 0 4px' },
  searchButton: {
    padding: '8px 20px', backgroundColor: '#FF9900', border: 'none',
    borderRadius: '0 4px 4px 0', fontWeight: 'bold', cursor: 'pointer'
  },

  // Stili per il pulsante minimalista
  filterWrapper: { position: 'relative', marginLeft: '15px', display: 'flex', alignItems: 'center' },
  filterIconButton: {
    cursor: 'pointer', backgroundColor: 'transparent', border: 'none',
    padding: '5px', display: 'flex', alignItems: 'center', outline: 'none'
  },

  filterPopover: {
    position: 'absolute', top: '130%', left: '50%', transform: 'translateX(-50%)',
    backgroundColor: 'white', width: '320px', padding: '20px', borderRadius: '8px',
    boxShadow: '0 4px 20px rgba(0,0,0,0.15)', zIndex: 1000, border: '1px solid #ddd',
  },
  popoverArrow: {
    position: 'absolute', top: '-10px', left: '50%', transform: 'translateX(-50%)',
    width: '0', height: '0', borderLeft: '10px solid transparent',
    borderRight: '10px solid transparent', borderBottom: '10px solid white',
  },
  filterSection: { marginBottom: '15px', display: 'flex', flexDirection: 'column' },
  sectionTitle: {
    fontSize: '12px', fontWeight: 'bold', color: '#555',
    marginBottom: '5px', textTransform: 'uppercase', letterSpacing: '1px'
  },
  priceInputGroup: {
    display: 'flex', alignItems: 'center', border: '1px solid #ccc',
    borderRadius: '4px', overflow: 'hidden', width: '100%', height: '40px',
  },
  priceInputMin: {
    flex: 1, width: '100px', padding: '8px', border: 'none',
    borderRight: '1px solid #ccc', outline: 'none', fontSize: '14px', textAlign: 'left',
  },
  priceInputMax: {
    flex: 1, width: '100px', padding: '8px', border: 'none',
    outline: 'none', fontSize: '14px', textAlign: 'left',
  },
  categorySelect: {
    padding: '8px', borderRadius: '4px', border: '1px solid #ccc',
    backgroundColor: 'white', fontSize: '14px', cursor: 'pointer', width: '100%'
  },
  rightActions: {
    display: 'flex',
    alignItems: 'center',
    marginLeft: 'auto',
    gap: '20px',
  },

  cartIconButton: {
    cursor: 'pointer',
    backgroundColor: 'transparent',
    border: 'none',
    padding: '5px',
    display: 'flex',
    alignItems: 'center',
    outline: 'none',
  },
};