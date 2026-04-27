export default function SearchBar({ onSearch }) {
  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Cerca prodotti..."
        onChange={(e) => onSearch(e.target.value)}
      />
    </div>
  );
}