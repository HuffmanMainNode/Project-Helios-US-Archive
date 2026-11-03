# CourtListener API Wrapper

`courtlistener_integration.py` is an optional, read-only search client for the CourtListener REST API.

## Configuration

Set `COURTLISTENER_API_KEY` in the environment or pass a token to `CourtListenerClient`. Do not commit credentials. The local archive and archive-audit utility do not require this token.

## Scope

The wrapper searches cases and normalizes a small set of returned fields. It is not a full crawler, does not archive opinions automatically, does not create source manifests, and does not establish that a result is controlling or current law.

## Safety boundaries

- Requests use a finite timeout.
- Search result limits are bounded.
- Unexpected response shapes are rejected.
- Returned case paths must be relative paths on the CourtListener host; external URLs are not accepted.
- API snippets are treated as untrusted text and stripped of markup before display.
- The wrapper does not write downloaded content to the archive.
