from crypto.hashing import create_hash


def verify_transaction_hash(transaction: dict) -> bool:
    """
    Verify that the current_hash matches the transaction data.

    The transaction must use the canonical protocol fields
    expected by the crypto layer.
    """

    if "current_hash" not in transaction:
        return False

    expected_hash = create_hash(transaction)

    return transaction["current_hash"] == expected_hash