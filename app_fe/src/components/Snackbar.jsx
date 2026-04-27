import { useState, useEffect, useImperativeHandle, forwardRef } from 'react';

const Snackbar = forwardRef((props, ref) => {
  const [show, setShow] = useState(false);
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);

  // Esponiamo il metodo "show" al mondo esterno
  useImperativeHandle(ref, () => ({
    show(msg, error = false) {
      setMessage(msg);
      setIsError(error);
      setShow(true);
      setTimeout(() => setShow(false), 3000); // Sparisce dopo 3 secondi
    }
  }));

  if (!show) return null;

  return (
    <div style={{
      ...styles.snackbar,
      backgroundColor: isError ? '#d32f2f' : '#388e3c',
      fontFamily: "'Roboto', sans-serif"
    }}>
      {message}
    </div>
  );
});

const styles = {
  snackbar: {
    position: 'fixed', bottom: '20px', left: '50%', transform: 'translateX(-50%)',
    padding: '12px 24px', color: 'white', borderRadius: '4px',
    zIndex: 9999, fontWeight: 'bold', boxShadow: '0 2px 5px rgba(0,0,0,0.2)'
  }
};

export default Snackbar;