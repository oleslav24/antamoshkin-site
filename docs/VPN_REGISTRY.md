# VPN portal: device draft registry

This phase records **device metadata only**. Creating a draft does not modify Xray or AmneziaWG, generate keys or grant VPN access.

## Cloudflare setup
1. Create a Cloudflare D1 database, e.g. `vpn_portal`.
2. Run the SQL from `migrations/0001_vpn_devices.sql` in the database's Console.
3. Under the Cloudflare **Pages project** settings, add a D1 binding named **VPN_DB** to the Production environment and select that database. Redeploy afterwards.
4. Keep **VPN_PORTAL_PASSWORD** as a secret. This is an admin preview: do not share the password with friends.

Without the binding, the device API fails closed with 503.

## Security boundaries
- Only labels, protocol, state and timestamps are stored. Never store VPN credentials or private configuration blobs in D1.
- POST uses the signed login session and checks same-origin.
- Current shared-password login lacks durable rate limiting and is not ready for public invitations. Individual identities, revocation, login throttling, stronger CSRF controls and an audit trail are needed before sending links to friends.
- No requests reach the VPN VPS. Provisioning remains disabled.
- 30-device cap is convenience, not an atomic concurrent quota.

## Next phase
Implement an authenticated least-privilege VPS service and validate the native Amnezia client update mechanism. Include transactional backups, rollback and reconciliation. Never expose Docker or arbitrary command execution over the Internet.
