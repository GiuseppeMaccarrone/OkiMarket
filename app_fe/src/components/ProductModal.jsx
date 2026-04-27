import React, { useState, useEffect } from 'react';
import { createProduct, getPresignedUrl, getCategories } from '../services/api';
import { useSnackbar } from '../context/SnackbarContext';

export default function ProductModal({ isOpen, onClose }) {
  const showSnackbar = useSnackbar();

  // Stato per memorizzare le categorie dal backend
  const [categories, setCategories] = useState([]);

  // Carichiamo le categorie ogni volta che la modale viene aperta
  useEffect(() => {
    if (isOpen) {
      const fetchCategories = async () => {
        try {
          const data = await getCategories();
          setCategories(data);
        } catch (err) {
          console.error("Errore caricamento categorie:", err);
          showSnackbar("Impossibile caricare le categorie", true);
        }
      };
      fetchCategories();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const file = formData.get('image');

    try {
      let imageUrl = null;

      if (file && file.size > 0) {
        const { url, file_path } = await getPresignedUrl(file.name, file.type);
        const uploadRes = await fetch(url, {
            method: 'PUT',
            body: file
        });

        if (!uploadRes.ok) throw new Error("Upload immagine fallito");
        imageUrl = file_path;
      }

      await createProduct({
        name: formData.get('name'),
        price: parseFloat(formData.get('price')),
        category_id: parseInt(formData.get('category_id')), // Legge il value della select
        tags: [],
        image_url: imageUrl
      });

      showSnackbar("Prodotto aggiunto con successo!");
      onClose();
    } catch (error) {
      console.error("Errore salvataggio:", error);
      showSnackbar("Errore: " + error.message, true);
    }
  };

  return (
    <div style={modalStyles.overlay}>
      <form onSubmit={handleSubmit} style={modalStyles.content}>
        <h2 style={{ margin: '0 0 10px 0' }}>Nuovo Prodotto</h2>

        <input name="name" placeholder="Nome Prodotto" required style={modalStyles.input} />

        <input name="price" type="number" step="0.01" placeholder="Prezzo" required style={modalStyles.input} />

        {/* Dropdown delle categorie */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
            <label style={{fontSize: '12px', color: '#666'}}>Categoria:</label>
            <select name="category_id" required style={modalStyles.categoryIinput}>
                <option value="">Seleziona una categoria...</option>
                {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>
                        {cat.name}
                    </option>
                ))}
            </select>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
            <label style={{fontSize: '12px', color: '#666'}}>Immagine Prodotto:</label>
            <input name="image" type="file" accept="image/*" style={modalStyles.fileInput} />
        </div>

        <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
          <button type="submit" style={modalStyles.btn}>Salva</button>
          <button type="button" onClick={onClose} style={modalStyles.cancelBtn}>Annulla</button>
        </div>
      </form>
    </div>
  );
}

const modalStyles = {
  overlay: {
    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.6)', zIndex: 2000,
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    fontFamily: "'Roboto', sans-serif"
  },
  content: {
    backgroundColor: 'white', padding: '25px', borderRadius: '12px',
    width: '380px', display: 'flex', flexDirection: 'column', gap: '15px',
    boxShadow: '0 8px 30px rgba(0,0,0,0.3)'
  },
  input: {
    padding: '12px', border: '1px solid #ccc', borderRadius: '4px',
    fontSize: '14px', fontFamily: "'Roboto', sans-serif", outlineColor: '#FF9900'
  },
  categoryIinput: {
    padding: '12px', border: '1px solid #ccc', borderRadius: '4px', paddingLeft: '6px',
    fontSize: '14px', fontFamily: "'Roboto', sans-serif", outlineColor: '#FF9900'
  },
  fileInput: { fontSize: '13px' },
  btn: {
    backgroundColor: '#FF9900', color: 'white', border: 'none',
    padding: '12px', cursor: 'pointer', borderRadius: '4px',
    fontWeight: 'bold', flex: 1, fontSize: '14px'
  },
  cancelBtn: {
    backgroundColor: '#eee', border: 'none', padding: '12px',
    cursor: 'pointer', borderRadius: '4px', flex: 1, fontSize: '14px'
  }
};