-- Cloudflare D1 metadata ONLY. Never store VPN keys, UUIDs or config blobs here.
CREATE TABLE IF NOT EXISTS vpn_devices (
  id TEXT PRIMARY KEY,
  label TEXT NOT NULL,
  protocol TEXT NOT NULL CHECK(protocol IN ('xray','awg')),
  state TEXT NOT NULL DEFAULT 'draft' CHECK(state IN ('draft','active','revoked')),
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS vpn_devices_created_idx ON vpn_devices(created_at);
