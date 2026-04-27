import { createCategory } from '../services/api';
import { useSnackbar } from '../context/SnackbarContext'; // Importiamo il contesto

export default function CategoryModal({ isOpen, onClose }) {
  const showSnackbar = useSnackbar();

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    const categoryName = e.target.name.value;
    try {
      await createCategory(categoryName);
      showSnackbar(`Categoria "${categoryName}" creata con successo!`);
      onClose();
    } catch (error) {
      console.error(error);
      showSnackbar("Errore durante il salvataggio della categoria", true);
    }
  };

  return (
    <div style={modalStyles.overlay}>
      <form onSubmit={handleSubmit} style={modalStyles.content}>
        <h2 style={{ margin: '0 0 10px 0' }}>Nuova Categoria</h2>

        <input name="name" placeholder="Nome Categoria" required style={modalStyles.input} />

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
    backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 2000,
    display: 'flex', alignItems: 'center', justifyContent: 'center'
  },
  content: {
    backgroundColor: 'white', padding: '25px', borderRadius: '8px',
    width: '350px', display: 'flex', flexDirection: 'column', gap: '12px'
  },
  input: { padding: '10px', border: '1px solid #ccc', borderRadius: '4px' },
  btn: {
    backgroundColor: '#FF9900', color: 'white', border: 'none',
    padding: '10px', cursor: 'pointer', borderRadius: '4px',
    fontWeight: 'bold', flex: 1
  },
  cancelBtn: {
    backgroundColor: '#eee', border: 'none', padding: '10px',
    cursor: 'pointer', borderRadius: '4px', flex: 1
  }
};