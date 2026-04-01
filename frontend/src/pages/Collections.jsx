import { useEffect, useState } from "react";
import {
  getCollections,
  createCollection,
  deleteCollection,
  removeDocketFromCollection,
} from "../api/collectionsApi";
import "../styles/collections.css";

export default function Collections() {
  const [collections, setCollections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [newCollectionName, setNewCollectionName] = useState("");
  const [error, setError] = useState("");
  const [unauthorized, setUnauthorized] = useState(false);

  const loadCollections = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await getCollections();
      setCollections(Array.isArray(data) ? data : []);
    } catch (err) {
      if (err.message === "UNAUTHORIZED") {
        setUnauthorized(true);
      } else {
        setError("Failed to load collections.");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCollections();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    const trimmedName = newCollectionName.trim();
    if (!trimmedName) return;

    setSubmitting(true);
    setError("");
    try {
      const created = await createCollection(trimmedName);
      setCollections((prev) => [
        ...prev,
        {
          collection_id: created.collection_id,
          name: trimmedName,
          docket_ids: [],
        },
      ]);
      setNewCollectionName("");
    } catch (err) {
      if (err.message === "UNAUTHORIZED") {
        setUnauthorized(true);
      } else {
        setError("Failed to create collection.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteCollection = async (collectionId) => {
    setError("");
    try {
      await deleteCollection(collectionId);
      setCollections((prev) =>
        prev.filter((col) => col.collection_id !== collectionId)
      );
    } catch (err) {
      if (err.message === "UNAUTHORIZED") {
        setUnauthorized(true);
      } else {
        setError("Failed to delete collection.");
      }
    }
  };

  const handleRemoveDocket = async (collectionId, docketId) => {
    setError("");
    try {
      await removeDocketFromCollection(collectionId, docketId);
      setCollections((prev) =>
        prev.map((col) =>
          col.collection_id === collectionId
            ? {
                ...col,
                docket_ids: (col.docket_ids || []).filter((id) => id !== docketId),
              }
            : col
        )
      );
    } catch (err) {
      if (err.message === "UNAUTHORIZED") {
        setUnauthorized(true);
      } else {
        setError("Failed to remove docket from collection.");
      }
    }
  };

  if (unauthorized) {
    return (
      <section className="collections-page">
        <h1 className="collections-title">My Collections</h1>
        <p>Please <a href="/login">log in</a> to view collections.</p>
      </section>
    );
  }

  return (
    <section className="collections-page">
      <div className="collections-header">
        <h1 className="collections-title">My Collections</h1>
        <form className="collections-create-form" onSubmit={handleCreate}>
          <input
            type="text"
            placeholder="New collection name"
            value={newCollectionName}
            onChange={(e) => setNewCollectionName(e.target.value)}
          />
          <button
            className="btn btn-primary"
            type="submit"
            disabled={submitting || !newCollectionName.trim()}
          >
            {submitting ? "Creating..." : "Create"}
          </button>
        </form>
      </div>

      {error && <p className="collections-error">{error}</p>}
      {loading ? (
        <p className="collections-muted">Loading collections...</p>
      ) : collections.length === 0 ? (
        <p className="collections-muted">
          No collections yet. Create your first one above.
        </p>
      ) : (
        <div className="collections-grid">
          {collections.map((collection) => {
            const docketIds = collection.docket_ids || [];
            return (
              <article key={collection.collection_id} className="collection-card">
                <div className="collection-card-top">
                  <h2>{collection.name}</h2>
                  <button
                    type="button"
                    className="collection-delete"
                    onClick={() => handleDeleteCollection(collection.collection_id)}
                  >
                    Delete
                  </button>
                </div>
                <p className="collection-count">
                  {docketIds.length} docket{docketIds.length === 1 ? "" : "s"}
                </p>

                {docketIds.length > 0 ? (
                  <ul className="collection-docket-list">
                    {docketIds.map((docketId) => (
                      <li key={docketId} className="collection-docket-item">
                        <span>{docketId}</span>
                        <button
                          type="button"
                          className="collection-remove-docket"
                          onClick={() =>
                            handleRemoveDocket(collection.collection_id, docketId)
                          }
                        >
                          Remove
                        </button>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="collections-muted">No dockets in this collection.</p>
                )}
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}
