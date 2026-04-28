import React, { useState, useEffect } from 'react';
import { getCategories, createCategory, updateCategory, deleteCategory } from '../services/api';
import { useSnackbar } from '../context/SnackbarContext';

export default function CategoryManagerModal({ isOpen, onClose }) {
  const showSnackbar = useSnackbar();
  const [categories, setCategories] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [editName, setEditName] = useState("");

  const refreshCategories = async () => {
    try {
      const data = await getCategories();
      setCategories(data);
    } catch (err) {
      showSnackbar("Errore nel caricamento categorie", true);
    }
  };

  useEffect(() => {
    if (isOpen) refreshCategories();
  }, [isOpen]);

  const handleUpdate = async (id) => {
    try {
      await updateCategory(id, editName);
      showSnackbar("Categoria aggiornata!");
      setEditingId(null);
      refreshCategories();
      // Lanciamo un evento per far aggiornare anche la Navbar
      window.dispatchEvent(new Event('categoriesUpdated'));
    } catch (err) {
      showSnackbar("Errore durante l'aggiornamento", true);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Sei sicuro? Se ci sono prodotti collegati il database darà errore.")) return;
    try {
      await deleteCategory(id);
      showSnackbar("Categoria eliminata con successo");
      refreshCategories();
      window.dispatchEvent(new Event('categoriesUpdated'));
    } catch (err) {
      showSnackbar("Errore: la categoria è probabilmente in uso", true);
    }
  };

  if (!isOpen) return null;

  return (
    <div style={modalStyles.overlay}>
      <div style={modalStyles.content}>
        <div style={modalStyles.header}>
            <h2 style={modalStyles.title}>Gestione Categorie</h2>
            <button onClick={onClose} style={modalStyles.closeX}>✕</button>
        </div>

        <div style={modalStyles.list}>
          {categories.map(cat => (
            <div key={cat.id} style={modalStyles.row}>
              {editingId === cat.id ? (
                <div style={{display: 'flex', flex: 1, gap: '10px'}}>
                  <input
                    style={modalStyles.miniInput}
                    value={editName}
                    onChange={(e) => setEditName(e.target.value)}
                    autoFocus
                  />
                  <button onClick={() => handleUpdate(cat.id)} style={modalStyles.saveBtn}>Salva</button>
                  <button onClick={() => setEditingId(null)} style={modalStyles.cancelBtn}>Annulla</button>
                </div>
              ) : (
                <>
                  <div style={modalStyles.catInfo}>
                    <span style={modalStyles.catName}>{cat.name}</span>
                    <small style={modalStyles.catId}>ID: {cat.id}</small>
                  </div>
                  <div style={modalStyles.actions}>
                    <button
                        onClick={() => {setEditingId(cat.id); setEditName(cat.name)}}
                        style={modalStyles.iconBtn}
                        title="Modifica"
                    >
                        ✎
                    </button>
                    <button
                        onClick={() => handleDelete(cat.id)}
                        style={modalStyles.deleteBtn}
                        title="Elimina"
                    >
                        🗑
                    </button>
                  </div>
                </>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

const modalStyles = {
  overlay: {
    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.6)', zIndex: 3000,
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    fontFamily: "'Roboto', sans-serif"
  },
  content: {
    backgroundColor: 'white', padding: '30px', borderRadius: '12px',
    width: '450px', maxHeight: '75vh', overflowY: 'auto',
    boxShadow: '0 10px 25px rgba(0,0,0,0.2)',
    display: 'flex', flexDirection: 'column'
  },
  header: {
    display: 'flex', justifyContent: 'space-between', alignItems: 'center',
    borderBottom: '2px solid #f0f2f2', paddingBottom: '15px', marginBottom: '10px'
  },
  title: { margin: 0, fontSize: '22px', color: '#232f3e' },
  closeX: {
    background: 'none', border: 'none', cursor: 'pointer',
    fontSize: '22px', color: '#555', padding: '5px'
  },
  list: { display: 'flex', flexDirection: 'column' },
  row: {
    display: 'flex', alignItems: 'center', padding: '15px 10px',
    borderBottom: '1px solid #eee', transition: 'background-color 0.2s'
  },
  catInfo: { display: 'flex', flexDirection: 'column', flex: 1 },
  catName: { fontSize: '24px', fontWeight: '500', color: '#111' },
  catId: { fontSize: '12px', color: '#888', marginTop: '2px' },
  actions: { display: 'flex', gap: '15px' },

  miniInput: {
    flex: 1, padding: '8px 12px', border: '2px solid #FF9900',
    borderRadius: '4px', outline: 'none', fontFamily: "'Roboto', sans-serif"
  },

  iconBtn: {
    background: 'none', border: 'none', cursor: 'pointer',
    fontSize: '32px', color: '#007185', display: 'flex', alignItems: 'center'
  },
  deleteBtn: {
    background: 'none', border: 'none', cursor: 'pointer',
    fontSize: '32px', color: '#CC0C39', display: 'flex', alignItems: 'center'
  },

  saveBtn: {
    backgroundColor: '#2ecc71', color: 'white', border: 'none',
    borderRadius: '4px', padding: '8px 12px', cursor: 'pointer', fontWeight: 'bold'
  },
  cancelBtn: {
    backgroundColor: '#95a5a6', color: 'white', border: 'none',
    borderRadius: '4px', padding: '8px 12px', cursor: 'pointer', fontWeight: 'bold'
  }
};