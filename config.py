"""
Configuration management for the trading ecosystem.
Uses environment variables with fallback defaults.
"""
import os
import logging
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ExchangeConfig:
    """Exchange-specific configuration"""
    name: str
    api_key: Optional[str] = None
    secret_key: Optional[str] = None
    sandbox_mode: bool = True
    
@dataclass
class TradingConfig:
    """Trading parameters"""
    risk_per_trade: float = 0.02  # 2% risk per trade
    max_position_size: float = 0.1  # 10% of portfolio
    max_open_positions: int = 5
    min_confidence_threshold: float = 0.65
    
@dataclass
class MLConfig:
    """Machine learning configuration"""
    train_test_split: float = 0.8
    validation_split: float = 0.2
    min_training_samples: int = 1000
    retrain_interval_hours: int = 24

class Config:
    """Main configuration class"""
    
    def __init__(self):
        # Exchange Configuration
        self.exchange = ExchangeConfig(
            name="binance",
            api_key=os.getenv("BINANCE_API_KEY"),
            secret_key=os.getenv("BINANCE_SECRET_KEY"),
            sandbox_mode=True  # Start in sandbox mode for safety
        )
        
        # Trading Configuration
        self.trading = TradingConfig(
            risk_per_trade=float(os.getenv("RISK_PER_TRADE", 0.02)),
            max_position_size=float(os.getenv("MAX_POSITION_SIZE", 0.1))
        )
        
        # ML Configuration
        self.ml = MLConfig()
        
        # Feature Engineering
        self.feature_windows = [5, 10, 20, 50, 100]
        self.indicators = ['sma', 'ema', 'rsi', 'macd', 'bollinger']
        
        # System Configuration
        self.data_collection_interval = 60  # seconds
        self.heartbeat_interval = 300  # seconds
        
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.exchange.sandbox_mode and (not self.exchange.api_key or not self.exchange.secret_key):
            logging.error("Live trading requires API keys")
            return False
        return True

# Global configuration instance
config = Config()