"""
Storage Service Layer
Handles JSON, SQLite, and MySQL storage for predictions
"""

import json
import sqlite3
import os
from datetime import datetime


class StorageService:
    """Service for storing and retrieving predictions"""
    
    def __init__(self, json_path=None, db_path=None, mysql_config=None):
        """
        Initialize storage service
        
        Args:
            json_path: Path to JSON history file
            db_path: Path to SQLite database file
            mysql_config: Dict with MySQL connection details:
                - host: MySQL server host
                - user: MySQL username
                - password: MySQL password
                - database: Database name
        """
        self.json_path = json_path or 'detection_history.json'
        self.db_path = db_path or 'predictions.db'
        self.mysql_config = mysql_config
        self.use_json = True
        self.use_sqlite = True
        self.use_mysql = False
        self.mysql_conn = None
        
        # Initialize MySQL if configured
        if mysql_config:
            self._init_mysql()
        
        # Initialize SQLite database
        self._init_sqlite()
    
    def _init_mysql(self):
        """Initialize MySQL connection and create table"""
        try:
            import mysql.connector
            
            print("\n[MySQL Init] Attempting connection...")
            print(f"  Host: {self.mysql_config.get('host', 'localhost')}")
            print(f"  User: {self.mysql_config.get('user', 'root')}")
            print(f"  Database: {self.mysql_config.get('database', 'crop_disease_db')}")
            
            # Test connection
            conn = mysql.connector.connect(
                host=self.mysql_config.get('host', 'localhost'),
                user=self.mysql_config.get('user', 'root'),
                password=self.mysql_config.get('password', ''),
                database=self.mysql_config.get('database', 'crop_disease_db')
            )
            
            print("[MySQL Init] ✅ Connection successful")
            
            cursor = conn.cursor()
            
            # Create table if not exists
            print("[MySQL Init] Creating table if not exists...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    image_path VARCHAR(255) NOT NULL,
                    disease VARCHAR(100) NOT NULL,
                    confidence FLOAT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            print("[MySQL Init] ✅ Table created/verified")
            
            conn.close()
            self.use_mysql = True
            print("[MySQL Init] ✅ MySQL storage enabled\n")
        
        except ImportError:
            print("[MySQL Init] ❌ mysql-connector-python not installed")
            print("     Install with: pip install mysql-connector-python\n")
            self.use_mysql = False
        except Exception as e:
            print(f"[MySQL Init] ❌ Connection failed: {type(e).__name__}: {str(e)}")
            print("     Falling back to SQLite and JSON storage\n")
            import traceback
            traceback.print_exc()
            self.use_mysql = False
    
    def _get_mysql_connection(self):
        """Get MySQL connection"""
        try:
            import mysql.connector
            
            print(f"  [MySQL] Connecting to {self.mysql_config.get('host')}...")
            print(f"    - User: {self.mysql_config.get('user')}")
            print(f"    - Database: {self.mysql_config.get('database')}")
            
            conn = mysql.connector.connect(
                host=self.mysql_config.get('host', 'localhost'),
                user=self.mysql_config.get('user', 'root'),
                password=self.mysql_config.get('password', ''),
                database=self.mysql_config.get('database', 'crop_disease_db')
            )
            
            print(f"  ✅ [MySQL] Connected successfully")
            return conn
        
        except ImportError as e:
            print(f"  ❌ [MySQL] ImportError: mysql-connector-python not installed")
            print(f"     Install with: pip install mysql-connector-python")
            return None
        except Exception as e:
            print(f"  ❌ [MySQL] Connection error: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _init_sqlite(self):
        """Initialize SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image_path TEXT NOT NULL,
                    disease TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Warning: Could not initialize SQLite database: {e}")
            self.use_sqlite = False
    
    def save_prediction(self, image_path, disease, confidence):
        """
        Save prediction to MySQL, SQLite, and JSON (with fallback)
        
        Args:
            image_path: Path to uploaded image
            disease: Disease name
            confidence: Confidence score
            
        Returns:
            Dict with:
                - 'success': bool
                - 'message': status message
        """
        try:
            # Validate and convert data types
            image_filename = os.path.basename(image_path)
            disease = str(disease).strip()
            confidence = float(confidence)  # Ensure float type (not numpy)
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            print("\n" + "="*60)
            print("SAVING PREDICTION")
            print("="*60)
            print(f"Image: {image_filename}")
            print(f"Disease: {disease}")
            print(f"Confidence: {confidence} (type: {type(confidence).__name__})")
            print(f"Timestamp: {timestamp}")
            print("="*60)
            
            # Try MySQL first (primary storage)
            if self.use_mysql:
                print("\n[MySQL] Attempting to save...")
                mysql_result = self._save_to_mysql(image_path, disease, confidence)
                if mysql_result:
                    print("✅ [MySQL] Saved successfully")
                else:
                    print("❌ [MySQL] Failed to save")
            else:
                print("\n[MySQL] Disabled or not configured")
            
            # Save to SQLite (secondary storage)
            if self.use_sqlite:
                print("\n[SQLite] Attempting to save...")
                sqlite_result = self._save_to_sqlite(image_path, disease, confidence)
                if sqlite_result:
                    print("✅ [SQLite] Saved successfully")
                else:
                    print("❌ [SQLite] Failed to save")
            else:
                print("\n[SQLite] Disabled")
            
            # Save to JSON (backward compatibility)
            if self.use_json:
                print("\n[JSON] Attempting to save...")
                json_result = self._save_to_json(image_path, disease, confidence, timestamp)
                if json_result:
                    print("✅ [JSON] Saved successfully")
                else:
                    print("❌ [JSON] Failed to save")
            else:
                print("\n[JSON] Disabled")
            
            print("="*60 + "\n")
            
            return {
                'success': True,
                'message': 'Prediction saved successfully'
            }
        
        except Exception as e:
            print(f"\n❌ ERROR in save_prediction: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'message': f'Error saving prediction: {str(e)}'
            }
    
    def _save_to_mysql(self, image_path, disease, confidence):
        """Save prediction to MySQL database"""
        try:
            print("  [MySQL] Getting connection...")
            conn = self._get_mysql_connection()
            if not conn:
                print("  ❌ [MySQL] Connection failed - returned None")
                return False
            
            print("  ✅ [MySQL] Connection established")
            cursor = conn.cursor()
            
            # Prepare data
            image_filename = os.path.basename(image_path)
            confidence_float = float(confidence)
            
            print(f"  [MySQL] Preparing INSERT query...")
            print(f"    - image_path: {image_filename}")
            print(f"    - disease: {disease}")
            print(f"    - confidence: {confidence_float}")
            
            # Execute insert
            cursor.execute('''
                INSERT INTO predictions (image_path, disease, confidence)
                VALUES (%s, %s, %s)
            ''', (image_filename, disease, confidence_float))
            
            print(f"  [MySQL] Query executed, rows affected: {cursor.rowcount}")
            
            # Commit transaction
            conn.commit()
            print(f"  ✅ [MySQL] Transaction committed")
            
            conn.close()
            return True
        
        except Exception as e:
            print(f"  ❌ [MySQL] Error: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _save_to_json(self, image_path, disease, confidence, timestamp):
        """Save prediction to JSON file"""
        try:
            print("  [JSON] Loading existing history...")
            history = self.load_history_json()
            print(f"  [JSON] Loaded {len(history)} existing records")
            
            image_filename = os.path.basename(image_path)
            confidence_rounded = round(float(confidence), 2)
            
            print(f"  [JSON] Adding new record...")
            history.insert(0, {
                'image': image_filename,
                'disease': disease,
                'confidence': confidence_rounded,
                'date': timestamp
            })
            
            # Keep only last 100 records
            history = history[:100]
            print(f"  [JSON] Total records after insert: {len(history)}")
            
            print(f"  [JSON] Writing to {self.json_path}...")
            with open(self.json_path, 'w') as f:
                json.dump(history, f, indent=2)
            
            print(f"  ✅ [JSON] Saved successfully")
            return True
        
        except Exception as e:
            print(f"  ❌ [JSON] Error: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _save_to_sqlite(self, image_path, disease, confidence):
        """Save prediction to SQLite database"""
        try:
            print("  [SQLite] Connecting to database...")
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            print(f"  ✅ [SQLite] Connected to {self.db_path}")
            
            image_filename = os.path.basename(image_path)
            confidence_float = float(confidence)
            
            print(f"  [SQLite] Preparing INSERT query...")
            print(f"    - image_path: {image_filename}")
            print(f"    - disease: {disease}")
            print(f"    - confidence: {confidence_float}")
            
            cursor.execute('''
                INSERT INTO predictions (image_path, disease, confidence)
                VALUES (?, ?, ?)
            ''', (image_filename, disease, confidence_float))
            
            print(f"  [SQLite] Query executed, rows affected: {cursor.rowcount}")
            
            conn.commit()
            print(f"  ✅ [SQLite] Transaction committed")
            
            conn.close()
            return True
        
        except Exception as e:
            print(f"  ❌ [SQLite] Error: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def load_history_json(self):
        """
        Load history from JSON file
        
        Returns:
            List of prediction records
        """
        try:
            if os.path.exists(self.json_path):
                with open(self.json_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load JSON history: {e}")
        
        return []
    
    def load_history_db(self, limit=100, source='mysql'):
        """
        Load history from database (MySQL preferred, fallback to SQLite)
        
        Args:
            limit: Maximum number of records to return
            source: 'mysql', 'sqlite', or 'auto' (try MySQL first)
            
        Returns:
            List of prediction records
        """
        # Try MySQL first if available
        if source in ['mysql', 'auto'] and self.use_mysql:
            records = self._load_from_mysql(limit)
            if records:
                return records
        
        # Fallback to SQLite
        if source in ['sqlite', 'auto'] and self.use_sqlite:
            return self._load_from_sqlite(limit)
        
        return []
    
    def _load_from_mysql(self, limit=100):
        """Load history from MySQL database"""
        try:
            conn = self._get_mysql_connection()
            if not conn:
                return []
            
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute('''
                SELECT id, image_path, disease, confidence, created_at
                FROM predictions
                ORDER BY created_at DESC
                LIMIT %s
            ''', (limit,))
            
            records = cursor.fetchall()
            conn.close()
            
            return records
        
        except Exception as e:
            print(f"Warning: Could not load from MySQL: {e}")
            return []
    
    def _load_from_sqlite(self, limit=100):
        """Load history from SQLite database"""
        try:
            if not self.use_sqlite:
                return []
            
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM predictions
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            records = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return records
        
        except Exception as e:
            print(f"Warning: Could not load from SQLite: {e}")
            return []
    
    def delete_prediction(self, image_filename):
        """
        Delete prediction from all storage layers
        
        Args:
            image_filename: Filename of image to delete
            
        Returns:
            Dict with success status
        """
        try:
            # Delete from MySQL
            if self.use_mysql:
                self._delete_from_mysql(image_filename)
            
            # Delete from SQLite
            if self.use_sqlite:
                self._delete_from_sqlite(image_filename)
            
            # Delete from JSON
            if self.use_json:
                history = self.load_history_json()
                history = [item for item in history if item['image'] != image_filename]
                with open(self.json_path, 'w') as f:
                    json.dump(history, f, indent=2)
            
            return {
                'success': True,
                'message': 'Prediction deleted successfully'
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error deleting prediction: {str(e)}'
            }
    
    def _delete_from_mysql(self, image_filename):
        """Delete prediction from MySQL"""
        try:
            conn = self._get_mysql_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            cursor.execute('DELETE FROM predictions WHERE image_path = %s', (image_filename,))
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"Warning: Could not delete from MySQL: {e}")
            return False
    
    def _delete_from_sqlite(self, image_filename):
        """Delete prediction from SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM predictions WHERE image_path = ?', (image_filename,))
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"Warning: Could not delete from SQLite: {e}")
            return False
    
    def clear_history(self):
        """
        Clear all history from all storage layers
        
        Returns:
            Dict with success status
        """
        try:
            # Clear MySQL
            if self.use_mysql:
                self._clear_mysql()
            
            # Clear SQLite
            if self.use_sqlite:
                self._clear_sqlite()
            
            # Clear JSON
            if self.use_json and os.path.exists(self.json_path):
                with open(self.json_path, 'w') as f:
                    json.dump([], f)
            
            return {
                'success': True,
                'message': 'History cleared successfully'
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error clearing history: {str(e)}'
            }
    
    def _clear_mysql(self):
        """Clear all records from MySQL"""
        try:
            conn = self._get_mysql_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            cursor.execute('DELETE FROM predictions')
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"Warning: Could not clear MySQL: {e}")
            return False
    
    def _clear_sqlite(self):
        """Clear all records from SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM predictions')
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"Warning: Could not clear SQLite: {e}")
            return False
