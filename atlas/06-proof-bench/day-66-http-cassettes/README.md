# Cassettes for Tool HTTP

**Day 66** · **Advanced** · Phase 06: Proof Bench: Evals and Harnesses

Record an HTTP tool once and replay the bytes so a later run does not touch the network.

## Concept

An agent tool that calls HTTP will score differently tomorrow if the server changes, and it will fail in a classroom with no network. This project wraps one tool, `get_status(dock_id)`, in a cassette. The first run, with a flag `record`, stores the URL, the query, and the response body under a key. Later runs with `replay` never open a socket. They return the stored body or fail with `cassette-miss`. A test uses a fake transport so recording does not need a real server. Replay must not call the transport at all, which you assert by counting calls. Editing the cassette body by hand is allowed only in a file you treat as source. The harness reads it. You will also show a miss: a dock id that was not recorded fails the replay run instead of falling through to the network.

## Approach

The cassette is a JSON map from a canonical request key to a body. The key includes the method, path, and sorted query. It does not include timestamps. The wrapper takes a transport function. In replay mode the wrapper does not receive a live transport, or it receives one that raises if called. Prefer the raise-if-called double so a mistake is loud. Record mode calls the transport once per distinct key and writes the file. A second record of the same key compares bodies and errors on conflict rather than silently overwriting. That conflict is how you notice an upstream that is not stable enough to cassette.

## Components

| Piece | Role |
| --- | --- |
| Canonical key | Method, path, and sorted query. |
| Cassette file | Map from key to response body. |
| Replay guard | Transport raises if replay tries to call it. |
| Conflict check | A second record with a different body errors. |

## How it works

1. Implement record and replay modes.
2. Record two dock ids using a fake transport.
3. Replay them and assert the transport call count is zero.
4. Replay a third id and assert `cassette-miss`.
5. Record the same key with a different body and assert conflict, leaving the file unchanged.

## Tech stack

- Python 3.11 or newer
- JSON cassette
- A fake transport in tests, no real HTTP required

## Setup

1. Create `cassettes/` with `cassette.py`, `fixtures/status.json`, and tests.
2. Run record, then replay, as two commands.
3. Run tests.
4. Add `cassettes/` output to the folder you would commit if this were a real suite, and say so in the notes.

## What done looks like

- Replay performs zero transport calls.
- An unknown key is a cassette miss, not a live call.
- Conflicting records do not overwrite the stored body.
- Request keys ignore field order in the query.

## Step ahead

A cassette can go stale when the server adds a field the agent starts to require. Add a schema version on the cassette and a checker that compares replayed bodies to a list of required JSON keys. A body missing `status` fails with `cassette-stale` rather than returning JSON the agent will misread as an empty dock. Fixture a recorded body from version 1 and a required-key list from version 2. The follow-on is detecting drift at replay time, before the agent treats a missing field as a real observation.
