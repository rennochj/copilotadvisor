"""Tests for configuration module."""

import sys
from pathlib import Path
from unittest.mock import mock_open, patch

# Add project root to sys.path for test discovery
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from document_collection.core.config import Configuration


class TestConfiguration:
    """Test configuration functionality."""

    def test_default_config(self):
        """Test default configuration values."""
        config = Configuration()

        assert config.get("destination_path") == "documents"  # Changed from "./output"
        assert config.get("convert_to_markdown") is True
        assert config.get("preserve_original") is False
        assert config.get("overwrite_existing") is False
        assert config.get("parallel_processing") is True

    def test_config_from_environment(self):
        """Test loading config from environment variables."""
        env_vars = {
            "DOCUMENT_COLLECTION_DEST": "/env/output",
            "DOCUMENT_COLLECTION_CONVERT": "false",
            "DOCUMENT_COLLECTION_WORKERS": "8",
        }

        with patch.dict("os.environ", env_vars):
            config = Configuration()

            assert config.get("destination_path") == "/env/output"
            assert config.get("convert_to_markdown") is False
            assert config.get("max_workers") == 8

    def test_config_from_file_yaml(self):
        """Test loading config from YAML file."""
        yaml_content = """
        destination_path: /yaml/output
        convert_to_markdown: false
        max_workers: 4
        """

        with patch("builtins.open", mock_open(read_data=yaml_content)):
            with patch("pathlib.Path.exists", return_value=True):
                config = Configuration("config.yaml")

                assert config.get("destination_path") == "/yaml/output"
                assert config.get("convert_to_markdown") is False
                assert config.get("max_workers") == 4

    def test_config_file_not_found(self):
        """Test handling of missing config file."""
        with patch("pathlib.Path.exists", return_value=False):
            # Should not raise an error, just use defaults
            config = Configuration("nonexistent.yaml")
            assert (
                config.get("destination_path") == "documents"
            )  # Changed from "./output"

    def test_config_get_method(self):
        """Test config get method with defaults."""
        config = Configuration()

        # Test existing key
        assert config.get("destination_path") == "documents"  # Changed from "./output"

        # Test non-existing key with default
        assert config.get("nonexistent_key", "default_value") == "default_value"

        # Test non-existing key without default
        assert config.get("nonexistent_key") is None

    def test_config_set_method(self):
        """Test config set method."""
        config = Configuration()

        config.set("custom_key", "custom_value")
        assert config.get("custom_key") == "custom_value"

        # Test overwriting existing key
        config.set("destination_path", "/new/path")
        assert config.get("destination_path") == "/new/path"

    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = Configuration()
        config_dict = config.get_all()

        assert isinstance(config_dict, dict)
        assert "destination_path" in config_dict
        assert "convert_to_markdown" in config_dict
        assert "preserve_original" in config_dict
