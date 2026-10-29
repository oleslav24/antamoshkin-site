-- A durable single-flight guard. A failed/uncertain attempt remains locked for reconciliation.
CREATE TABLE IF NOT EXISTS vpn_provision_attempts (
  device_id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  state TEXT NOT NULL DEFAULT 'started',
  error_code TEXT
);
