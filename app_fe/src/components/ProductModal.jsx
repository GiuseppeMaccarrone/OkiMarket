import React, { useState, useEffect } from 'react';
import { createProduct, updateProduct, getPresignedUrl, getCategories } from '../services/api';
import { useSnackbar } from '../context/SnackbarContext';

export default function ProductModal({ isOpen, onClose, initialData = null, onRefresh }) {
  const showSnackbar = useSnackbar();
  const [categories, setCategories] = useState([]);

  // Stati per la gestione dei Tags
  const [tempTags, setTempTags] = useState([]);
  const [tagInput, setTagInput] = useState("");

  const isEdit = !!initialData;

  useEffect(() => {
    if (isOpen) {
      fetchCategories();
      // Se siamo in modifica, carichiamo i tag esistenti
      setTempTags(initialData?.tags || []);
    } else {
      // Reset dei tag alla chiusura
      setTempTags([]);
      setTagInput("");
    }
  }, [isOpen, initialData]);

  const fetchCategories = async () => {
    try {
      const data = await getCategories();
      setCategories(data);
    } catch (err) {
      console.error("Errore categorie:", err);
    }
  };

  // Funzione per aggiungere un tag alla lista temporanea
  const handleAddTag = (e) => {
    e.preventDefault();
    const trimmedTag = tagInput.trim().toLowerCase();
    if (trimmedTag && !tempTags.includes(trimmedTag)) {
      setTempTags([...tempTags, trimmedTag]);
      setTagInput("");
    }
  };

  // Funzione per rimuovere un tag dalla lista temporanea
  const handleRemoveTag = (tagToRemove) => {
    setTempTags(tempTags.filter(tag => tag !== tagToRemove));
  };

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const file = formData.get('image');

    try {
      let imageUrl = initialData?.image_url || null;

      if (file && file.size > 0) {
        const { url, file_path } = await getPresignedUrl(file.name, file.type);
        const uploadRes = await fetch(url, { method: 'PUT', body: file });
        if (!uploadRes.ok) throw new Error("Upload immagine fallito");
        imageUrl = file_path;
      }

      const productPayload = {
        name: formData.get('name'),
        price: parseFloat(formData.get('price')),
        category_id: parseInt(formData.get('category_id')),
        tags: tempTags, // Inviamo la lista di tag aggiornata
        image_url: imageUrl
      };

      if (isEdit) {
        await updateProduct(initialData.id, productPayload);
        showSnackbar("Prodotto aggiornato!");
      } else {
        await createProduct(productPayload);
        showSnackbar("Prodotto creato!");
      }

      onRefresh?.();
      onClose();
    } catch (error) {
      showSnackbar("Errore: " + error.message, true);
    }
  };

  return (
    <div style={modalStyles.overlay}>
      <form onSubmit={handleSubmit} style={modalStyles.content}>
        <h2 style={modalStyles.modalTitle}>
          {isEdit ? "Modifica Prodotto" : "Nuovo Prodotto"}
        </h2>

        <input name="name" defaultValue={initialData?.name || ""} placeholder="Nome Prodotto" required style={modalStyles.input} />

        <input name="price" type="number" step="0.01" defaultValue={initialData?.price || ""} placeholder="Prezzo" required style={modalStyles.input} />

        <div style={modalStyles.fieldGroup}>
            <label style={modalStyles.label}>Categoria:</label>
            <select name="category_id" defaultValue={initialData?.category_id || ""} required style={modalStyles.input}>
                <option value="">Seleziona categoria...</option>
                {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>{cat.name}</option>
                ))}
            </select>
        </div>

        {/* --- SEZIONE TAGS --- */}
        <div style={modalStyles.fieldGroup}>
            <label style={modalStyles.label}>Tags:</label>
            <div style={modalStyles.tagInputContainer}>
                <input
                    style={modalStyles.tagInput}
                    placeholder="Aggiungi tag..."
                    value={tagInput}
                    onChange={(e) => setTagInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleAddTag(e)}
                />
                <button type="button" onClick={handleAddTag} style={modalStyles.addTagBtn}>+</button>
            </div>

            <div style={modalStyles.tagList}>
                {tempTags.map((tag, index) => (
                    <div key={index} style={modalStyles.tagBadge}>
                        #{tag}
                        <span onClick={() => handleRemoveTag(tag)} style={modalStyles.removeTagX}>✕</span>
                    </div>
                ))}
            </div>
        </div>

        <div style={modalStyles.fieldGroup}>
            <label style={modalStyles.label}>
                {isEdit ? "Cambia immagine (opzionale):" : "Immagine Prodotto:"}
            </label>
            <input name="image" type="file" accept="image/*" style={modalStyles.fileInput} />
        </div>

        <div style={modalStyles.buttonRow}>
          <button type="submit" style={modalStyles.btn}>{isEdit ? "Aggiorna" : "Salva"}</button>
          <button type="button" onClick={onClose} style={modalStyles.cancelBtn}>Annulla</button>
        </div>
      </form>
    </div>
  );
}

const modalStyles = {
  overlay: { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.6)', zIndex: 5000, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: "'Roboto', sans-serif" },
  content: { backgroundColor: 'white', padding: '25px', borderRadius: '12px', width: '400px', display: 'flex', flexDirection: 'column', gap: '15px', boxShadow: '0 8px 30px rgba(0,0,0,0.3)', maxHeight: '90vh', overflowY: 'auto' },
  modalTitle: { margin: '0 0 5px 0', fontSize: '22px', color: '#111' },
  fieldGroup: { display: 'flex', flexDirection: 'column', gap: '5px' },
  label: { fontSize: '13px', color: '#666', fontWeight: 'bold' },
  input: { padding: '12px', border: '1px solid #ccc', borderRadius: '4px', fontSize: '14px', outlineColor: '#FF9900' },

  // Stili per i Tags
  tagInputContainer: { display: 'flex', gap: '5px' },
  tagInput: { flex: 1, padding: '10px', border: '1px solid #ccc', borderRadius: '4px', fontSize: '14px' },
  addTagBtn: { backgroundColor: '#FF9900', color: 'white', border: 'none', borderRadius: '4px', width: '40px', fontSize: '20px', cursor: 'pointer', fontWeight: 'bold' },
  tagList: { display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '5px' },
  tagBadge: { backgroundColor: '#e7f4f5', color: '#007185', padding: '4px 10px', borderRadius: '4px', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '6px', border: '1px solid #007185' },
  removeTagX: { cursor: 'pointer', fontWeight: 'bold', fontSize: '14px', marginLeft: '4px', color: '#CC0C39' },

  fileInput: { fontSize: '13px' },
  buttonRow: { display: 'flex', gap: '10px', marginTop: '10px' },
  btn: { backgroundColor: '#FF9900', color: 'white', border: 'none', padding: '12px', cursor: 'pointer', borderRadius: '4px', fontWeight: 'bold', flex: 1 },
  cancelBtn: { backgroundColor: '#eee', border: 'none', padding: '12px', cursor: 'pointer', borderRadius: '4px', flex: 1 }
};