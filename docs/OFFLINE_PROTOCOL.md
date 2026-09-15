# MONEY-MATE Offline Payment Protocol

## 1. Purpose

MONEY-MATE demonstrates cryptographically verifiable offline transaction
integrity and replay/tamper detection in a simulated payment environment.

This is a hackathon prototype.

It is not:
- UPI
- UPI Lite
- a bank wallet
- a production payment rail
- a replacement for a regulated payment system

---

## 2. Offline Transaction

Every offline transaction contains the following fields:

| Field | Description |
|---|---|
| version | Protocol version |
| wallet_id | Identifier of the wallet creating the transaction |
| transaction_id | Unique UUID for the transaction |
| counter | Monotonically increasing transaction counter |
| timestamp | Transaction creation time in UTC |
| currency | Currency code |
| amount_minor | Amount represented in minor currency units |
| recipient_identifier | Recipient or merchant identifier |
| payment_mode | Payment mode, e.g. OFFLINE |
| previous_hash | Hash of the previous transaction |
| current_hash | SHA-256 hash of the current transaction |
| key_id | Identifier of the signing key |
| signature | Ed25519 digital signature |

---

## 3. Transaction Version

The current protocol version is:

version = 1

The canonical serialization format must not be changed silently.

Any incompatible format change must increment the protocol version.

---

## 4. Monetary Representation

MONEY-MATE uses integer minor units for monetary values.

For INR:

- Currency = INR
- Minor unit = paise

Examples:

₹10.00 = 1000 paise

₹150.00 = 15000 paise

₹999.50 = 99950 paise

Floating-point monetary values must not be used inside the cryptographic payload.

---

## 5. Transaction ID

The transaction ID must be a unique UUID.

The recommended representation is a lowercase canonical UUID string.

Example:

550e8400-e29b-41d4-a716-446655440000

The transaction ID must not be generated using only:
- timestamp
- amount + timestamp
- incrementing counter

The counter and transaction ID serve different purposes.

---

## 6. Timestamp

Transaction timestamps use UTC.

Canonical format:

YYYY-MM-DDTHH:MM:SSZ

Example:

2026-09-15T05:45:00Z

Second-level precision is used for the prototype.

---

## 7. Canonical Serialization

The security payload fields must always be serialized in this exact order:

1. version
2. wallet_id
3. transaction_id
4. counter
5. timestamp
6. currency
7. amount_minor
8. recipient_identifier
9. payment_mode
10. previous_hash

### 7.1 Exact Serialization Format

For protocol version 1, the canonical transaction payload uses
UTF-8 text in the following exact format:

version=<version>
wallet_id=<wallet_id>
transaction_id=<transaction_id>
counter=<counter>
timestamp=<timestamp>
currency=<currency>
amount_minor=<amount_minor>
recipient_identifier=<recipient_identifier>
payment_mode=<payment_mode>
previous_hash=<previous_hash>

Each field is represented as:

key=value

Rules:

1. Fields MUST appear in exactly the order specified above.
2. Fields MUST be separated by exactly one LF (`\n`) character.
3. There MUST be no trailing LF (`\n`) after the final field.
4. The complete serialized text MUST be encoded as UTF-8 bytes.
5. Integer values MUST use decimal digits without leading zeros.
6. `amount_minor` MUST be an integer.
7. `timestamp` MUST use UTC format `YYYY-MM-DDTHH:MM:SSZ`.
8. `previous_hash` MUST be represented as lowercase hexadecimal.
9. String fields MUST NOT contain LF (`\n`) or CR (`\r`) characters.
10. The serialization MUST NOT depend on dictionary/map ordering.
11. Python and Dart implementations MUST produce identical canonical UTF-8 bytes for the same transaction.
12. `currency` MUST consist of exactly three uppercase ASCII letters.
13. `payment_mode` MUST use a predefined uppercase value such as `OFFLINE`.
14. `wallet_id` and `transaction_id` MUST use lowercase canonical UUID strings.
15. `recipient_identifier` MUST contain only ASCII letters, digits, `_`, `-`, `.`, and `:`.
16. No field value may contain `\n` or `\r`.
### 7.2 Example

Given:

version = 1
wallet_id = 550e8400-e29b-41d4-a716-446655440000
transaction_id = 123e4567-e89b-12d3-a456-426614174000
counter = 1
timestamp = 2026-09-15T05:45:00Z
currency = INR
amount_minor = 15000
recipient_identifier = merchant_demo_001
payment_mode = OFFLINE
previous_hash = 0000000000000000000000000000000000000000000000000000000000000000

The canonical serialized text is:

version=1
wallet_id=550e8400-e29b-41d4-a716-446655440000
transaction_id=123e4567-e89b-12d3-a456-426614174000
counter=1
timestamp=2026-09-15T05:45:00Z
currency=INR
amount_minor=15000
recipient_identifier=merchant_demo_001
payment_mode=OFFLINE
previous_hash=0000000000000000000000000000000000000000000000000000000000000000

This exact text is encoded using UTF-8 before being passed to the
hashing process.

## 8. String Encoding

Canonical textual serialization uses UTF-8 encoding.

Identifiers should use strict, deterministic representations.

The system must not silently normalize signed fields differently between the client and backend.

---

## 9. Genesis Hash

The first transaction uses the following genesis hash:

0000000000000000000000000000000000000000000000000000000000000000

The genesis hash is exactly 64 hexadecimal zero characters.

---

## 10. Hash Algorithm

MONEY-MATE uses SHA-256.

For a transaction:

current_hash = SHA256(previous_hash_bytes || canonical_transaction_data)

Where:

- `||` means byte concatenation.
- `previous_hash_bytes` is the UTF-8 encoding of the lowercase hexadecimal `previous_hash` string.
- `canonical_transaction_data` is the exact canonical serialization encoded as UTF-8.
- SHA-256 is applied to the resulting concatenated bytes.
- `current_hash` is represented as lowercase hexadecimal.

Therefore:

previous_hash_bytes =
UTF8(previous_hash)

canonical_transaction_data =
UTF8(canonical_serialization)

hash_input =
previous_hash_bytes || canonical_transaction_data

current_hash =
SHA256(hash_input)

The backend must independently reconstruct the canonical serialization
and recompute the expected hash.
---

## 11. Digital Signature

MONEY-MATE uses Ed25519 digital signatures.

The signature is created over the transaction hash:

signature = Sign(private_key, transaction_hash)

The backend verifies:

Verify(public_key, transaction_hash, signature)

Private keys must never be sent to the backend.

---

## 12. Key Identifier

Every wallet signing key has a `key_id`.

Example:

wallet-key-v1

The transaction contains the `key_id`.

The backend associates the key ID with the wallet and its registered public key.

---

## 13. Monotonic Counter

Each wallet maintains a monotonically increasing transaction counter.

Example:

TX1 → counter 1

TX2 → counter 2

TX3 → counter 3

Invalid examples include:

1 → 2 → 2

1 → 3 → 2

The backend validates counter progression.

---

## 14. Replay Protection

The backend maintains server-side records of processed:

- transaction IDs
- transaction counters

The backend rejects:

- duplicate transaction IDs
- previously processed transactions
- reused counters
- invalid counter sequences

Example error:

REPLAY_DETECTED

---

## 15. Offline Spending Limits

Offline spending must be controlled using configurable limits.

Example demo configuration:

- Maximum offline transaction = ₹500
- Daily offline limit = ₹2,000

The exact values must remain configurable.

---

## 16. Offline Transaction States

Transactions may have the following states:

- CREATED_OFFLINE
- PENDING_SYNC
- SYNCING
- SYNCED
- REJECTED
- TAMPERED
- REPLAYED

An offline transaction is not considered server-finalized until synchronization succeeds.

---

## 17. Offline Transaction Creation

When creating an offline transaction:

1. Check device/network state.
2. Check local available balance.
3. Check offline transaction limit.
4. Validate recipient.
5. Increment the counter.
6. Construct the transaction.
7. Set `previous_hash`.
8. Canonically serialize the transaction.
9. Compute the SHA-256 hash.
10. Sign the hash using Ed25519.
11. Persist the transaction locally.
12. Update local ledger state.
13. Mark the transaction as `PENDING_SYNC`.

---

## 18. Local Balance

The system distinguishes between:

- AVAILABLE LOCAL BALANCE
- SERVER-CONFIRMED BALANCE

The local offline state must not be treated as authoritative server state.

---

## 19. Synchronization

When network connectivity returns:

Flutter collects pending transactions and sends them to:

POST /api/v1/offline/sync

The backend independently performs:

1. Hash verification
2. Signature verification
3. Counter validation
4. Replay detection
5. Wallet/key validation
6. Reconciliation

Each transaction receives an individual result.

---

## 20. Important Security Principle

The backend must never trust the client-provided hash.

The backend reconstructs the canonical transaction payload and independently calculates:

expected_hash

It then compares:

expected_hash == submitted current_hash

Only after hash verification should signature verification continue.

---

## 21. Error Codes

The protocol supports the following security-related error codes:

- HASH_MISMATCH
- INVALID_SIGNATURE
- UNKNOWN_KEY
- REPLAY_DETECTED
- COUNTER_GAP
- COUNTER_ROLLBACK
- INVALID_COUNTER
- INVALID_TRANSACTION
- WALLET_MISMATCH
- KEY_WALLET_MISMATCH
- TRANSACTION_ALREADY_SYNCED
- OFFLINE_LIMIT_EXCEEDED
- STALE_TRANSACTION
- INVALID_CANONICAL_FORMAT

---

## 22. Security Limitations

This prototype does not fully protect against:

- compromised operating systems
- rooted or jailbroken devices
- stolen private keys
- malicious hardware
- advanced device cloning
- full offline double-spend attacks
- compromised trusted execution environments

A local hash chain alone does not solve all offline double-spending scenarios.

The prototype mitigates risk using:

- offline spending limits
- local balance reservation
- monotonic counters
- wallet/device binding
- server reconciliation
- replay detection
- signed transactions

---

## 23. Protocol Change Rule

Once Flutter and backend integration begins, do not randomly change:

- transaction fields
- field order
- serialization
- hash algorithm
- signature algorithm
- error codes

If a protocol change is required, update this document and the cryptographic test vectors immediately.