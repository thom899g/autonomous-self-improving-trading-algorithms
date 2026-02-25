"""
Firebase Firestore client for state management and real-time data streaming.
CRITICAL: All database and state management uses Firebase as required.
"""
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.exceptions import FirebaseError

class FirebaseClient:
    """Firebase Firestore client for the trading ecosystem"""
    
    def __init__(self, config):
        self.config = config
        self.db = None
        self._initialize_firebase()
        
    def _initialize_firebase(self) -> None:
        """Initialize Firebase connection"""
        try:
            # Check if Firebase app is already initialized
            if not firebase_admin._apps:
                # Initialize with service account credentials from environment
                cred_dict = {
                    "type": "service_account",
                    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
                    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
                
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            logging.info("Firebase Firestore initialized successfully")
            
        except (ValueError, FirebaseError) as e:
            logging.error(f"Failed to initialize Firebase: {e}")
            raise
            
        except Exception as e:
            logging.error(f"Unexpected error initializing Firebase: {e}")
            raise
    
    def store_market_data(self, symbol: str, timeframe: str, data: Dict[str, Any]) -> bool:
        """Store market data in Firestore"""
        try:
            if not self.db:
                logging.error("Firestore not initialized")
                return False
            
            collection_path = f"market_data/{symbol}/{timeframe}"
            doc_ref = self.db.collection(collection_path).document(str(data['timestamp']))
            doc_ref.set(data)
            return True
            
        except Exception as e:
            logging.error(f"Error storing market data: {e}")
            return False
    
    def store_strategy(self, strategy_id: str,