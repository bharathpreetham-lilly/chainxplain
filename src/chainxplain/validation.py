"""Input validation utilities for ChainXplain."""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Exception raised for validation errors."""
    pass


def validate_ethereum_address(address: str) -> str:
    """
    Validate and normalize an Ethereum address.
    
    Args:
        address: The address to validate
        
    Returns:
        Normalized address (lowercase with 0x prefix)
        
    Raises:
        ValidationError: If address is invalid
    """
    if not address:
        raise ValidationError("Address cannot be empty")
    
    # Remove whitespace
    address = address.strip()
    
    # Check format
    if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
        raise ValidationError(
            f"Invalid Ethereum address format: {address}. "
            "Expected 42 characters starting with 0x"
        )
    
    # Normalize to lowercase
    normalized = address.lower()
    logger.debug(f"Validated address: {normalized}")
    return normalized


def validate_transaction_hash(tx_hash: str) -> str:
    """
    Validate and normalize a transaction hash.
    
    Args:
        tx_hash: The transaction hash to validate
        
    Returns:
        Normalized transaction hash (lowercase with 0x prefix)
        
    Raises:
        ValidationError: If transaction hash is invalid
    """
    if not tx_hash:
        raise ValidationError("Transaction hash cannot be empty")
    
    # Remove whitespace
    tx_hash = tx_hash.strip()
    
    # Check format
    if not re.match(r'^0x[a-fA-F0-9]{64}$', tx_hash):
        raise ValidationError(
            f"Invalid transaction hash format: {tx_hash}. "
            "Expected 66 characters starting with 0x"
        )
    
    # Normalize to lowercase
    normalized = tx_hash.lower()
    logger.debug(f"Validated transaction hash: {normalized}")
    return normalized


def validate_chain_name(chain: str, supported_chains: Optional[list] = None) -> str:
    """
    Validate and normalize a blockchain name.
    
    Args:
        chain: The chain name to validate
        supported_chains: List of supported chain names (optional)
        
    Returns:
        Normalized chain name (lowercase)
        
    Raises:
        ValidationError: If chain name is invalid
    """
    if not chain:
        raise ValidationError("Chain name cannot be empty")
    
    # Remove whitespace and normalize
    chain = chain.strip().lower()
    
    # Check against supported chains if provided
    if supported_chains:
        if chain not in [c.lower() for c in supported_chains]:
            raise ValidationError(
                f"Unsupported chain: {chain}. "
                f"Supported chains: {', '.join(supported_chains)}"
            )
    
    # Basic sanity check - alphanumeric and hyphens only
    if not re.match(r'^[a-z0-9-]+$', chain):
        raise ValidationError(
            f"Invalid chain name format: {chain}. "
            "Only lowercase letters, numbers, and hyphens allowed"
        )
    
    logger.debug(f"Validated chain: {chain}")
    return chain


def sanitize_string_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitize string input for safe processing.
    
    Args:
        text: The text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
        
    Raises:
        ValidationError: If input is too long or contains invalid characters
    """
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Check length
    if len(text) > max_length:
        raise ValidationError(
            f"Input too long: {len(text)} characters (max: {max_length})"
        )
    
    # Remove any null bytes
    text = text.replace('\x00', '')
    
    # Check for SQL injection patterns (basic check)
    suspicious_patterns = [
        r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b)',
        r'(--|\;|\/\*|\*\/)',
        r'(<script|javascript:)',
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            logger.warning(f"Suspicious pattern detected in input: {pattern}")
            raise ValidationError("Input contains potentially unsafe content")
    
    return text


def validate_positive_integer(value: int, max_value: Optional[int] = None, 
                             field_name: str = "value") -> int:
    """
    Validate a positive integer.
    
    Args:
        value: The value to validate
        max_value: Maximum allowed value (optional)
        field_name: Name of the field for error messages
        
    Returns:
        The validated integer
        
    Raises:
        ValidationError: If value is invalid
    """
    if not isinstance(value, int):
        raise ValidationError(f"{field_name} must be an integer")
    
    if value < 1:
        raise ValidationError(f"{field_name} must be positive")
    
    if max_value and value > max_value:
        raise ValidationError(
            f"{field_name} exceeds maximum: {value} > {max_value}"
        )
    
    return value
