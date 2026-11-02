# A Read-Only Field Notebook Protocol

**Day 95** · **Advanced** · Phase 08: Frontier Lab

Expose local markdown notes through two tools, search and get, with a schema and no write path.

## Concept

Agents need a narrow way to read your notes. This project defines a small protocol: a process receives a JSON request and returns a JSON response. The only methods are `search` and `get`. `search` takes a query and returns heading matches with ids. `get` takes an id and returns that section's text. There is no method that writes, deletes, or shells out. A request with method `write` returns an error code `unknown-method` and does not touch the filesystem except to append a log line if you choose to log. You will implement the server in one module and a client function that sends a request dict. Transport can be in-process. The protocol shape is what you are practicing, the same shape a Model Context Protocol server uses, without building a price tracker or a review scraper.

## Approach

The notebook is a folder of markdown files with headings. Ids are stable: file path plus heading slug. `search` is BM25 or a simple substring scan over headings, and you document which. `get` returns the section body and refuses an id it did not issue. A test calls `get` with a path traversal such as `../secrets.md` and expects an error, not a file read outside the notebook root. Resolve ids through a table you built, not through string concatenation onto a base path. That choice is the security-relevant part of an otherwise read-only toy, and the test is required.

## Components

| Piece | Role |
| --- | --- |
| Request schema | Method name and arguments. |
| Search method | Returns ids and headings from the notebook only. |
| Get method | Returns a section by an issued id. |
| Unknown-method error | Any other method, including write. |

## How it works

1. Index the notebook into an id table.
2. Serve `search` and `get` in-process.
3. Reject `write` without changing a source file's mtime. A test can record mtimes.
4. Reject a traversal id.
5. Log requests as method names only, without dumping full section bodies into the log.

## Tech stack

- Python 3.11 or newer
- Local markdown notebook
- JSON requests and responses

## Setup

1. Create `notebook-protocol/` with `server.py`, `notebook/`, and tests.
2. Run a scripted client session: search, then get.
3. Run the rejection tests.
4. Describe the two methods in `protocol.md` in a few lines a caller could implement.

## What done looks like

- Search then get returns a real section from your notebook.
- `write` does not modify source files.
- An id outside the issued table does not read an arbitrary path.
- The log does not store full section bodies.

## Step ahead

A write path will be requested. Add a third method, `propose_edit`, that writes a patch file under `proposals/` and never modifies the notebook. The patch file contains the id and the suggested text. A test asserts the notebook file hash is unchanged and the proposal file exists. `propose_edit` on an unknown id writes nothing. The follow-on is a suggestion that cannot be confused with a saved edit.
