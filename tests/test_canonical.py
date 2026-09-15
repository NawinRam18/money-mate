from crypto.canonical import serialize_transaction_text


GENESIS_HASH = "0" * 64


def test_canonical_serialization_exact_format():
    transaction = {
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

    expected = (
        "version=1\n"
        "wallet_id=550e8400-e29b-41d4-a716-446655440000\n"
        "transaction_id=123e4567-e89b-12d3-a456-426614174000\n"
        "counter=1\n"
        "timestamp=2026-09-15T05:45:00Z\n"
        "currency=INR\n"
        "amount_minor=15000\n"
        "recipient_identifier=merchant_demo_001\n"
        "payment_mode=OFFLINE\n"
        "previous_hash="
        + GENESIS_HASH
    )

    actual = serialize_transaction_text(transaction)

    assert actual == expected


def test_canonical_serialization_has_no_trailing_newline():
    transaction = {
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

    result = serialize_transaction_text(transaction)

    assert not result.endswith("\n")
    assert not result.endswith("\r")


def test_genesis_hash_is_64_lowercase_hex_characters():
    assert len(GENESIS_HASH) == 64
    assert GENESIS_HASH == "0" * 64
    