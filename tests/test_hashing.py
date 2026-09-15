from crypto.hashing import create_hash, verify_hash


GENESIS_HASH = "0" * 64


def make_transaction():
    return {
        "version": 1,
        "wallet_id": "550e8400-e29b-41d4-a716-446655440000",
        "transaction_id": "123e4567-e89b-12d3-a456-426614174000",
        "counter": 1,
        "timestamp": "2026-09-15T05:45:00Z",
        "currency": "INR",
        "amount_minor": 15000,
        "recipient_identifier": "merchant_demo_001",
        "payment_mode": "OFFLINE",
        "previous_hash": GENESIS_HASH,
    }


def test_create_hash_returns_64_lowercase_hex_characters():
    transaction = make_transaction()

    result = create_hash(transaction)

    assert len(result) == 64
    assert result == result.lower()

    # Make sure every character is hexadecimal.
    int(result, 16)


def test_same_transaction_produces_same_hash():
    transaction1 = make_transaction()
    transaction2 = make_transaction()

    hash1 = create_hash(transaction1)
    hash2 = create_hash(transaction2)

    assert hash1 == hash2


def test_changing_amount_changes_hash():
    transaction = make_transaction()

    original_hash = create_hash(transaction)

    transaction["amount_minor"] = 150000

    modified_hash = create_hash(transaction)

    assert modified_hash != original_hash


def test_verify_hash_accepts_correct_hash():
    transaction = make_transaction()

    transaction["current_hash"] = create_hash(transaction)

    assert verify_hash(transaction) is True


def test_verify_hash_rejects_modified_transaction():
    transaction = make_transaction()

    transaction["current_hash"] = create_hash(transaction)

    # Tamper with the amount after the hash was created.
    transaction["amount_minor"] = 999999

    assert verify_hash(transaction) is False


def test_deterministic_hash_test_vector():
    transaction = make_transaction()

    expected_hash = (
        "fcdd65c1cf65fadf11cd59c3bfd181518dbb404c8d0f4774348b751f87733c89"
    )

    assert create_hash(transaction) == expected_hash