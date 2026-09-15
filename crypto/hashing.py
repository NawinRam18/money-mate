import hashlib
import re

from crypto.canonical import serialize_transaction


def _validate_previous_hash(previous_hash: str) -> None:
    """Make sure previous_hash is exactly 64 lowercase hexadecimal characters."""
    if not isinstance(previous_hash, str):
        raise ValueError("previous_hash must be a string")

    if not re.fullmatch(r"[0-9a-f]{64}", previous_hash):
        raise ValueError(
            "previous_hash must be 64 lowercase hexadecimal characters"
        )


def create_hash(transaction: dict) -> str:
    """
    Create the current hash for a transaction.

    Protocol:
        hash_input =
            UTF-8(previous_hash)
            +
            UTF-8(canonical_transaction_data)

        current_hash = SHA-256(hash_input)

    The result is returned as lowercase hexadecimal.
    """

    previous_hash = transaction["previous_hash"]

    _validate_previous_hash(previous_hash)

    # Convert the previous hash text into UTF-8 bytes.
    previous_hash_bytes = previous_hash.encode("utf-8")

    # Convert the canonical transaction into UTF-8 bytes.
    canonical_transaction_data = serialize_transaction(transaction)

    # Join the two byte sequences exactly as specified by the protocol.
    hash_input = previous_hash_bytes + canonical_transaction_data

    # Calculate SHA-256.
    digest = hashlib.sha256(hash_input).hexdigest()

    return digest


def verify_hash(transaction: dict) -> bool:
    """
    Verify that the transaction's current_hash matches
    the hash calculated from its contents.

    Returns True if the hash is correct.
    Returns False if it does not match.
    """

    if "current_hash" not in transaction:
        return False

    expected_hash = create_hash(transaction)

    return transaction["current_hash"] == expected_hash