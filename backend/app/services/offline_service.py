import hashlib
import json


def generate_hash(transaction_data: dict, previous_hash: str) -> str:
    data = {
        "transaction": transaction_data,
        "previous_hash": previous_hash
    }

    canonical_data = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":")
    )

    return hashlib.sha256(
        canonical_data.encode()
    ).hexdigest()


def verify_hash(
    transaction_data: dict,
    previous_hash: str,
    current_hash: str
) -> bool:
    expected_hash = generate_hash(
        transaction_data,
        previous_hash
    )

    return expected_hash == current_hash