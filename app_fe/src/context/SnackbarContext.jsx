import { createContext, useContext, useRef } from 'react';
import Snackbar from '../components/Snackbar';

const SnackbarContext = createContext();

export const SnackbarProvider = ({ children }) => {
  const snackbarRef = useRef();

  const showSnackbar = (msg, isError) => {
    snackbarRef.current?.show(msg, isError);
  };

  return (
    <SnackbarContext.Provider value={showSnackbar}>
      {children}
      <Snackbar ref={snackbarRef} />
    </SnackbarContext.Provider>
  );
};

export const useSnackbar = () => useContext(SnackbarContext);