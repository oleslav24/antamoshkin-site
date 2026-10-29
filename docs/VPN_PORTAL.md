# VPN portal: phase 1 (safe preview)

This is an **unmerged prototype** for Cloudflare Pages. No VPN account creation is enabled. It does not call or modify the production VPS.

## Deployment prerequisite

Configure a strong **Cloudflare Pages environment secret** named `VPN_PORTAL_PASSWORD` (minimum 24 characters). Do not store the password in this repository, static assets, logs or commit history. Functions fail closed (503) when it is missing. The access middleware guards `/vpn/*` and `/api/vpn/*`. The login page is public, but authenticated VPN pages and API routes require a signed, one-hour HttpOnly cookie.

**Important:** this shared-password preview is *not production-ready access control*. Before inviting friends, replace it with individual identities/invitations, persistent rate limiting, credential revocation, audit logs, CSRF protection, and Cloudflare WAF/Access policies. Do not merge or deploy without security review. If Pages builds use a static-only deployment pipeline, verify that Pages Functions are actually deployed.

## Phase 2: VPS integration (not implemented)

* A dedicated, least-privilege provisioning service on VPS, reachable only by authenticated server-to-server transport (e.g. Cloudflare Tunnel + Access service token).
* Durable per-device database; separate identities and device quotas.
* Atomic backups, rollback and locking around Amnezia-managed `clientsTable` and protocol configs.
* Xray: VLESS UUID and protocol-specific client export; preserve existing Reality keys, SNI, short IDs, port 8443 and user-selected fingerprint firefox.
* AWG 3.1.20260812: unique keys, available IP, 3.1 obfuscation parameters, runtime peer application and persisted `clientsTable`.
* Reconcile with AmneziaVPN's native management workflow before writing any configs, to avoid it overwriting portal changes.
* QR and one-time configuration delivery only after access controls are complete.

Never commit `server.json`, `awg0.conf`, `clientsTable`, private keys, URLs containing credentials, or VPS backups.
