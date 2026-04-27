import { createProduct, getPresignedUrl } from '../services/api';
import { useSnackbar } from '../context/SnackbarContext';

export default function ProductModal({ isOpen, onClose }) {
  // 1. Gli HOOKS vanno SEMPRE chiamati in cima, prima di qualsiasi return o if!
  const showSnackbar = useSnackbar();

  // 2. Solo DOPO gli hooks puoi fare il controllo di apertura
  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const file = formData.get('image');

    try {
      let imageUrl = null;

      if (file && file.size > 0) {
        // Richiesta URL presignato
        const { url, file_path } = await getPresignedUrl(file.name, file.type);

        // Upload a MinIO
        const uploadRes = await fetch(url, {
            method: 'PUT',
            body: file
        });

        if (!uploadRes.ok) throw new Error("Upload immagine fallito");
        imageUrl = file_path;
      }

      // Creazione Prodotto
      await createProduct({
        name: formData.get('name'),
        price: parseFloat(formData.get('price')),
        category_id: parseInt(formData.get('category_id')),
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
        <input name="category_id" type="number" placeholder="ID Categoria" required style={modalStyles.input} />

        <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
            <label style={{fontSize: '12px', color: '#666'}}>Immagine Prodotto:</label>
            <input name="image" type="file" accept="image/*" />
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
  overlay: { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 2000, display: 'flex', alignItems: 'center', justifyContent: 'center' },
  content: { backgroundColor: 'white', padding: '25px', borderRadius: '8px', width: '350px', display: 'flex', flexDirection: 'column', gap: '12px' },
  input: { padding: '10px', border: '1px solid #ccc', borderRadius: '4px' },
  btn: { backgroundColor: '#FF9900', color: 'white', border: 'none', padding: '10px', cursor: 'pointer', borderRadius: '4px', fontWeight: 'bold', flex: 1 },
  cancelBtn: { backgroundColor: '#eee', border: 'none', padding: '10px', cursor: 'pointer', borderRadius: '4px', flex: 1 }
};