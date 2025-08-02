"""Configuration management for document collection."""

import os
from pathlib import Path
from typing import Any, Dict

import yaml

from .types import (
    DEFAULT_BATCH_SIZE,
    DEFAULT_DESTINATION,
    DEFAULT_MAX_WORKERS,
    DEFAULT_RETRY_ATTEMPTS,
    DEFAULT_RETRY_DELAY,
    DEFAULT_TIMEOUT,
    ConfigDict,
)


class Configuration:
    """Configuration manager for document collection."""
    
    def __init__(self, config_file: str | Path | None = None) -> None:
        """
        Initialize configuration.
        
        Args:
            config_file: Optional path to configuration file
        """
        self._config: ConfigDict = {}
        self._load_defaults()
        
        if config_file:
            self._load_from_file(config_file)
        
        self._load_from_environment()
    
    def _load_defaults(self) -> None:
        """Load default configuration values."""
        self._config = {
            # General settings
            "destination_path": str(DEFAULT_DESTINATION),
            "convert_to_markdown": True,
            "preserve_original": False,
            "overwrite_existing": False,
            
            # Processing settings
            "parallel_processing": True,
            "max_workers": DEFAULT_MAX_WORKERS,
            "batch_size": DEFAULT_BATCH_SIZE,
            
            # Retry settings
            "retry_attempts": DEFAULT_RETRY_ATTEMPTS,
            "retry_delay": DEFAULT_RETRY_DELAY,
            "retry_exponential_backoff": True,
            
            # Network settings
            "timeout": DEFAULT_TIMEOUT,
            "user_agent": "DocumentCollection/0.1.0",
            "follow_redirects": True,
            "verify_ssl": True,
            
            # Conversion settings
            "markdown_header_metadata": True,
            "preserve_formatting": True,
            "extract_images": True,
            "image_directory": "images",
            
            # Logging settings
            "log_level": "INFO",
            "log_to_file": False,
            "log_file": "document_collection.log",
            
            # Validation settings
            "validate_inputs": True,
            "check_file_exists": True,
            "check_url_reachable": False,  # Can be slow
            
            # Storage settings
            "create_directories": True,
            "directory_permissions": 0o755,
            "file_permissions": 0o644,
        }
    
    def _load_from_file(self, config_file: str | Path) -> None:
        """
        Load configuration from file.
        
        Args:
            config_file: Path to configuration file
        """
        config_path = Path(config_file)
        
        if not config_path.exists():
            return
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.suffix.lower() in ['.yml', '.yaml']:
                    file_config = yaml.safe_load(f)
                else:
                    # Assume it's a simple key=value format
                    file_config = {}
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            file_config[key.strip()] = value.strip()
            
            if file_config:
                self._config.update(file_config)
                
        except Exception as e:
            # Log error but don't fail - use defaults
            print(f"Warning: Could not load config file {config_file}: {e}")
    
    def _load_from_environment(self) -> None:
        """Load configuration from environment variables."""
        env_mapping = {
            "DOCUMENT_COLLECTION_DEST": "destination_path",
            "DOCUMENT_COLLECTION_CONVERT": "convert_to_markdown",
            "DOCUMENT_COLLECTION_PRESERVE": "preserve_original",
            "DOCUMENT_COLLECTION_OVERWRITE": "overwrite_existing",
            "DOCUMENT_COLLECTION_WORKERS": "max_workers",
            "DOCUMENT_COLLECTION_TIMEOUT": "timeout",
            "DOCUMENT_COLLECTION_RETRY_ATTEMPTS": "retry_attempts",
            "DOCUMENT_COLLECTION_RETRY_DELAY": "retry_delay",
            "DOCUMENT_COLLECTION_LOG_LEVEL": "log_level",
            "DOCUMENT_COLLECTION_USER_AGENT": "user_agent",
        }
        
        for env_var, config_key in env_mapping.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                # Convert string values to appropriate types
                if config_key in ["max_workers", "retry_attempts"]:
                    try:
                        self._config[config_key] = int(env_value)
                    except ValueError:
                        pass
                elif config_key in ["timeout", "retry_delay"]:
                    try:
                        self._config[config_key] = float(env_value)
                    except ValueError:
                        pass
                elif config_key in ["convert_to_markdown", "preserve_original", "overwrite_existing"]:
                    self._config[config_key] = env_value.lower() in ["true", "1", "yes", "on"]
                else:
                    self._config[config_key] = env_value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
    
    def get_all(self) -> ConfigDict:
        """
        Get all configuration values.
        
        Returns:
            Dictionary of all configuration values
        """
        return self._config.copy()
    
    def update(self, config: ConfigDict) -> None:
        """
        Update configuration with new values.
        
        Args:
            config: Dictionary of configuration values to update
        """
        self._config.update(config)
    
    def save_to_file(self, config_file: str | Path) -> None:
        """
        Save current configuration to file.
        
        Args:
            config_file: Path to save configuration file
        """
        config_path = Path(config_file)
        
        # Create directory if it doesn't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            if config_path.suffix.lower() in ['.yml', '.yaml']:
                yaml.dump(self._config, f, default_flow_style=False, indent=2)
            else:
                # Save as key=value format
                for key, value in self._config.items():
                    f.write(f"{key}={value}\n")
    
    @property
    def destination_path(self) -> Path:
        """Get destination path as Path object."""
        return Path(self.get("destination_path", DEFAULT_DESTINATION))
    
    @property
    def max_workers(self) -> int:
        """Get maximum number of workers."""
        return self.get("max_workers", DEFAULT_MAX_WORKERS)
    
    @property
    def timeout(self) -> float:
        """Get timeout in seconds."""
        return self.get("timeout", DEFAULT_TIMEOUT)
    
    @property
    def retry_attempts(self) -> int:
        """Get number of retry attempts."""
        return self.get("retry_attempts", DEFAULT_RETRY_ATTEMPTS)
    
    @property
    def retry_delay(self) -> float:
        """Get retry delay in seconds."""
        return self.get("retry_delay", DEFAULT_RETRY_DELAY)


# Global configuration instance
_global_config: Configuration | None = None


def get_config() -> Configuration:
    """Get global configuration instance."""
    global _global_config
    if _global_config is None:
        _global_config = Configuration()
    return _global_config


def set_config(config: Configuration) -> None:
    """Set global configuration instance."""
    global _global_config
    _global_config = config


def reset_config() -> None:
    """Reset global configuration to defaults."""
    global _global_config
    _global_config = Configuration()
