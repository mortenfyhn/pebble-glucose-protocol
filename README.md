# Pebble Glucose Protocol

A small AppMessage protocol for pushing glucose data to a Pebble watchface, so that watchfaces and data
sources can be developed and released independently of each other.

The watchface announces which fields it can display; the sender pushes those fields and nothing else.
A new watchface needs no changes on the sender side, and a new sender needs no changes to the
watchface.

**[Read the spec →](PEBBLE_GLUCOSE_PROTOCOL.md)**

## Status

Draft v1, in use daily on real hardware, with three implementations (listed at the end of the spec).
Not finished: the sender-rendered bitmap slots are reserved and deliberately unspecified, and the
whole thing is open to revision while it is young.

## Using it

Copy [`protocol.h`](protocol.h) into your project — it is header-only with nothing to build. Key
numbers are frozen once published, so a copy can fall behind but cannot silently disagree. There is no
package, submodule or dependency to take on.

Senders need the same numbers in whatever language they are written in; there is no shared file for
that yet.

## Scope

Pebble-specific and glucose-specific, deliberately. AppMessage's few-hundred-bytes-per-update budget
and the watches' power constraints shape the field choices — pre-formatted strings rather than
numbers, one byte per graph point — so this is not trying to be a general watch protocol.

It is not tied to any particular data source. xDrip, a pump read directly over BLE, or the watch's own
firmware are all just senders.

## License

[Zero-Clause BSD](https://opensource.org/license/0bsd): You can do anything you want, no attribution needed.
