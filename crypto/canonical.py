import re
from datetime import datetime
from uuid import UUID


CANONICAL_FIELDS = (
    "version",
    "wallet_id",
    "transaction_id",
    "counter",
    "timestamp",
    "currency",
    "amount_minor",
    "recipient_identifier",
    "payment_mode",
    "previous_hash",
)


def _validate_no_newlines(value: str, field_name: str) -> None:
    """Make sure a field does not contain newline characters."""
    if "\n" in value or "\r" in value:
        raise ValueError(f"{field_name} cannot contain newline characters")


def _validate_uuid(value: str, field_name: str) -> None:
    """Make sure the UUID is lowercase canonical UUID format."""
    try:
        parsed = UUID(value)
    except ValueError:
        raise ValueError(f"{field_name} must be a valid UUID")

    if str(parsed) != value:
        raise ValueError(
            f"{field_name} must use lowercase canonical UUID format"
        )


def _validate_timestamp(value: str) -> None:
    """Make sure the timestamp follows the required UTC format."""
    if not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",
        value,
    ):
        raise ValueError(
            "timestamp must use UTC format YYYY-MM-DDTHH:MM:SSZ"
        )

    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise ValueError("timestamp is not a valid UTC timestamp")


def _validate_transaction(transaction: dict) -> None:
    """Validate all fields required for canonical serialization."""

    # Check that every required field exists.
    for field in CANONICAL_FIELDS:
        if field not in transaction:
            raise ValueError(f"Missing required field: {field}")

    # version
    if type(transaction["version"]) is not int:
        raise ValueError("version must be an integer")

    if transaction["version"] != 1:
        raise ValueError("Unsupported protocol version")

    # wallet_id
    if not isinstance(transaction["wallet_id"], str):
        raise ValueError("wallet_id must be a string")

    _validate_no_newlines(transaction["wallet_id"], "wallet_id")
    _validate_uuid(transaction["wallet_id"], "wallet_id")

    # transaction_id
    if not isinstance(transaction["transaction_id"], str):
        raise ValueError("transaction_id must be a string")

    _validate_no_newlines(
        transaction["transaction_id"],
        "transaction_id",
    )
    _validate_uuid(
        transaction["transaction_id"],
        "transaction_id",
    )

    # counter
    if type(transaction["counter"]) is not int:
        raise ValueError("counter must be an integer")

    if transaction["counter"] < 1:
        raise ValueError("counter must be greater than or equal to 1")

    # timestamp
    if not isinstance(transaction["timestamp"], str):
        raise ValueError("timestamp must be a string")

    _validate_no_newlines(transaction["timestamp"], "timestamp")
    _validate_timestamp(transaction["timestamp"])

    # currency
    if not isinstance(transaction["currency"], str):
        raise ValueError("currency must be a string")

    _validate_no_newlines(transaction["currency"], "currency")

    if not re.fullmatch(r"[A-Z]{3}", transaction["currency"]):
        raise ValueError(
            "currency must contain exactly three uppercase ASCII letters"
        )

    # amount_minor
    if type(transaction["amount_minor"]) is not int:
        raise ValueError("amount_minor must be an integer")

    if transaction["amount_minor"] < 0:
        raise ValueError("amount_minor cannot be negative")

    # recipient_identifier
    if not isinstance(transaction["recipient_identifier"], str):
        raise ValueError("recipient_identifier must be a string")

    _validate_no_newlines(
        transaction["recipient_identifier"],
        "recipient_identifier",
    )

    if not re.fullmatch(
        r"[A-Za-z0-9_.:\-]+",
        transaction["recipient_identifier"],
    ):
        raise ValueError(
            "recipient_identifier contains invalid characters"
        )

    # payment_mode
    if not isinstance(transaction["payment_mode"], str):
        raise ValueError("payment_mode must be a string")

    _validate_no_newlines(
        transaction["payment_mode"],
        "payment_mode",
    )

    if not re.fullmatch(
        r"[A-Z][A-Z0-9_]*",
        transaction["payment_mode"],
    ):
        raise ValueError(
            "payment_mode must use an uppercase predefined value"
        )

    # previous_hash
    if not isinstance(transaction["previous_hash"], str):
        raise ValueError("previous_hash must be a string")

    _validate_no_newlines(
        transaction["previous_hash"],
        "previous_hash",
    )

    if not re.fullmatch(
        r"[0-9a-f]{64}",
        transaction["previous_hash"],
    ):
        raise ValueError(
            "previous_hash must be 64 lowercase hexadecimal characters"
        )


def serialize_transaction_text(transaction: dict) -> str:
    """
    Create the exact canonical transaction text.

    The field order is fixed by CANONICAL_FIELDS.
    Fields are separated by exactly one newline.
    There is no trailing newline.
    """

    _validate_transaction(transaction)

    lines = [
        f"version={transaction['version']}",
        f"wallet_id={transaction['wallet_id']}",
        f"transaction_id={transaction['transaction_id']}",
        f"counter={transaction['counter']}",
        f"timestamp={transaction['timestamp']}",
        f"currency={transaction['currency']}",
        f"amount_minor={transaction['amount_minor']}",
        f"recipient_identifier={transaction['recipient_identifier']}",
        f"payment_mode={transaction['payment_mode']}",
        f"previous_hash={transaction['previous_hash']}",
    ]

    return "\n".join(lines)


def serialize_transaction(transaction: dict) -> bytes:
    """
    Return the canonical transaction as UTF-8 bytes.
    """

    canonical_text = serialize_transaction_text(transaction)
    return canonical_text.encode("utf-8")