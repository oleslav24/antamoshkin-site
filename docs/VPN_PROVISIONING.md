# VPN provisioning integration (draft)
The web portal is an authenticated ADMIN console, not a friends-facing portal. Never share the shared admin password with guests.

## Deployment prerequisites
1. Run migration `migrations/0002_vpn_provision_attempts.sql` on production D1 `vpn_portal`.
2. Deploy the VPS service at a non-public localhost listener and attach a Cloudflare Tunnel with access restrictions. The backend must expose exactly `POST /v1/xray/provision`, requiring a high-entropy bearer token via Authorization and enforcing idempotency by device UUID.
3. In the correct Pages project `antamoshkin-site`, set encrypted environment variables `VPN_PROVISION_URL` (tunnel HTTPS origin, without trailing slash) and `VPN_PROVISION_TOKEN` (random high-entropy bearer token). Do not commit credentials.
4. Deploy the new Pages commit only AFTER the VPS backend is ready. Until then `/api/vpn/create` returns 503 and never provisions a device.

## Protocol
Request: `POST /v1/xray/provision`, headers Authorization Bearer secret and Idempotency-Key equal to the D1 UUID. JSON `{"id":"<D1 UUID>","label":"Phone"}`.
Response: `{"device_id":"<D1 UUID>","vpn":"vpn://..."}`. No plaintext secret or private key in server logs. Restrict request body and return size.

The service must **durably** map idempotency keys to created Xray UUIDs, safely back up and validate the config, restart/rollback without changing other clients, and derive the native guest profile from an official `.vpn` template. Never allow arbitrary commands, paths, config or UUID from the HTTP request.

## Failure recovery
`vpn_provision_attempts` is a durable single-flight lock. If a call fails or times out, leave the attempt locked rather than retrying blindly; reconcile the VPS idempotency ledger and D1 state manually. A successful request marks D1 device active but does not persist its `.vpn` secret; the browser can download it only in that immediate response. Plan safe authenticated re-issue and revocation in a later change.

Threat model: shared portal password, no rate limiting, single-admin use only, origin-checked POST, secret-bearing response Cache-Control no-store. Tighten login throttling, access controls and individual permissions before exposing to friends.
