const API_BASE_URL = 'http://localhost:8000/api/v1';

// --- PRODOTTI ---
export const getProducts = async (params = {}) => {
  const backendParams = {};
  if (params.search) backendParams.search = params.search;
  if (params.minPrice) backendParams.min_price = params.minPrice;
  if (params.maxPrice) backendParams.max_price = params.maxPrice;
  if (params.category_id) backendParams.category_id = params.category_id;
  if (params.sort) backendParams.sort_by = params.sort;
  backendParams.skip = params.skip || 0;
  backendParams.limit = params.limit || 4;

  const queryString = new URLSearchParams(backendParams).toString();
  const response = await fetch(`${API_BASE_URL}/products/list?${queryString}`);
  if (!response.ok) throw new Error('Errore nel recupero prodotti');
  return await response.json();
};

export const getProductById = async (id) => {
  const response = await fetch(`${API_BASE_URL}/products/get_by_id/${id}`);
  if (!response.ok) throw new Error('Prodotto non trovato');
  return await response.json();
};

export const createProduct = async (productData) => {
  const response = await fetch(`${API_BASE_URL}/products/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(productData)
  });
  if (!response.ok) throw new Error('Errore creazione prodotto');
  return await response.json();
};

// --- CATEGORIE ---
export const createCategory = async (name) => {
  const response = await fetch(`${API_BASE_URL}/categories/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  });
  if (!response.ok) throw new Error('Errore creazione categoria');
  return await response.json();
};

export const getCategories = async () => {
  const response = await fetch(`${API_BASE_URL}/categories/list`);
  if (!response.ok) throw new Error('Errore nel recupero categorie');
  return await response.json();
};

// --- UTILITY IMMAGINI ---
export const getPresignedUrl = async (fileName, fileType) => {
  const response = await fetch(`${API_BASE_URL}/storage/presigned-url?file_name=${fileName}`);
  if (!response.ok) throw new Error('Errore recupero URL upload');
  return await response.json();
};