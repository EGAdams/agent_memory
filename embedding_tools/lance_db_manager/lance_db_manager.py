import os
import lancedb
import pandas as pd
import pyarrow as pa

class LanceDBManager:
    """Manages data storage in LanceDB."""

    def __init__(self, database_directory, table_name ):
        if not os.path.exists( database_directory ): # *** ERROR if database directory is not found
            raise FileNotFoundError( f"Database directory not found: { database_directory }" )
    
        db_path=f"{ database_directory }/lancedb"
        self.LANCEDB_TABLE_NAME = table_name
        self.db = lancedb.connect(os.path.expanduser(db_path))
        self.table_name = self.LANCEDB_TABLE_NAME
        self.table = self.setup_table()

    def setup_table(self):
        """Initialize or open the LanceDB table."""
        schema = pa.schema([
            pa.field("id", pa.string()),
            pa.field("vector", pa.list_(pa.float32(), 1536)),
            pa.field("filepath", pa.string()),
            pa.field("time", pa.float64()),
            pa.field("nexus_path", pa.string())  # Path to stored java function
        ])

        if self.table_name in self.db.table_names():
            return self.db.open_table(self.table_name)
        return self.db.create_table(self.table_name, schema=schema)

    def store_embeddings(self, data):
        """Insert embeddings into the LanceDB table."""
        df = pd.DataFrame(data)
        self.table.add(df)

    def search_embeddings(self, query_embedding, top_k=5):
        """Search the nearest neighbors in LanceDB using vector search."""
        results = self.table.search(query_embedding).limit(top_k).to_pandas()
        return results["id"].tolist()  # Return a list of matching function IDs
    
    def delete_entry(self, unique_id):
        """Delete an entry from LanceDB using the unique ID."""
        try:
            self.table.delete(filter=f"id = '{unique_id}'")
            print(f"Deleted entry {unique_id} from LanceDB.")
            return True
        except Exception as e:
            print(f"Error deleting entry {unique_id} from LanceDB: {e}")
            return False