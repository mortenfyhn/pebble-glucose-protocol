# Pebble Glucose Protocol

**Draft of Version 1**

This is a protocol for sending glucose/CGM data to a Pebble watchface over [AppMessages](https://developer.repebble.com/docs/c/Foundation/AppMessage/).

- Sender: Anything with glucose data and a Pebble connection (xDrip, a custom app, or something else).
- Watchface: Any Pebble watchface implementing this protocol.

Each watchface has a UUID, which the sender must target. To support arbitrary watchfaces the sender must let the user set the watchface UUID.

## Communication flow

1. On launch and reconnect, the watchface sends a capability announcement.
1. The sender stores the capabilities and responds with the corresponding data.
1. The sender sends new data when it has any.
1. The watchface can re-send its announcement any time to request a full refresh.

## Message keys: Capability announcement (watchface 🡒 sender)

| Key | Name                    | Type   | Description |
|-----|-------------------------|--------|-------------|
| 0   | KEY_PROTOCOL_VERSION    | uint8  | Protocol version (increment for breaking changes) |
| 1   | KEY_CAPABILITIES        | uint32 | Watchface capability bitfield, see below |
| 2   | KEY_GRAPH_HOURS         | uint8  | Hours of graph history, set 0 to disable |
| 3-9 |                         |        | *Reserved* |

Watchfaces can re-send the announcement any time to request a full update from the sender.

Capability bits:

| Name               | Mask   | Description |
|--------------------|--------|-------------|
| CAP_BG             | `0x01` | Timestamped BG value |
| CAP_TREND_ARROW    | `0x02` | Trend arrow |
| CAP_DELTA          | `0x04` | Delta |
| CAP_IOB            | `0x08` | IOB |
| CAP_STATUS         | `0x10` | Status line |
| CAP_SENDER_BATTERY | `0x20` | Sender battery |

## Message keys: Main data (sender 🡒 watchface)

| Key   | Name                  | Type   | Description |
|-------|-----------------------|--------|-------------|
| 10    | KEY_BG_TIMESTAMP      | uint32 | BG reading timestamp (Unix epoch seconds) |
| 11    | KEY_BG_STRING         | string | Formatted BG value in sender's units (e.g. "5.7" or "103") |
| 12    | KEY_DELTA_STRING      | string | Formatted BG delta (e.g. "-0.3" or "-5.6") |
| 13    | KEY_TREND_ARROW       | uint8  | Trend arrow index (see below) |
| 14    | KEY_IOB_STRING        | string | Formatted insulin-on-board (e.g. "2.5") |
| 15    | KEY_STATUS_STRING     | string | Any sensor/pump status text (e.g. "PUMP SUSPENDED") |
| 16    | KEY_SENDER_BATTERY    | uint8  | Sender battery level (0–100) |
| 17    | KEY_STATUS_START      | uint32 | Start time of current status, can be used to display a count-up timer (Unix epoch seconds) |
| 18    | KEY_STATUS_END        | uint32 | End time of current status, can be used to display a count-down timer (Unix epoch seconds) |
| 19-29 |                       |        | *Reserved* |

A status should never have more than one timer (KEY_STATUS_START or KEY_STATUS_END or neither).

Trend arrow indices:

| Name              | Index | Description |
|-------------------|-------|-------------|
| TREND_UNKNOWN     | 0     | Unknown     |
| TREND_FLAT        | 1     | Flat        |
| TREND_SLANT_UP    | 2     | Slant up    |
| TREND_SLANT_DOWN  | 3     | Slant down  |
| TREND_UP          | 4     | Up          |
| TREND_DOWN        | 5     | Down        |
| TREND_DOUBLE_UP   | 6     | Double up   |
| TREND_DOUBLE_DOWN | 7     | Double down |
| TREND_TRIPLE_UP   | 8     | Triple up   |
| TREND_TRIPLE_DOWN | 9     | Triple down |

## Message keys: Raw graph (sender 🡒 watchface)

| Key   | Name                  | Type   | Description |
|-------|-----------------------|--------|-------------|
| 30    | KEY_GRAPH_DATA        | bytes  | Raw graph data, see below |
| 31    | KEY_GRAPH_HIGH_LINE   | uint8  | High BG threshold (mg/dL / 2) |
| 32    | KEY_GRAPH_LOW_LINE    | uint8  | Low BG threshold (mg/dL / 2) |
| 33-39 |                       |        | *Reserved* |

Graph data can cover a single new point, the full GRAPH_HOURS history, or anything in
between. Watchfaces merge incoming data into their graph data buffer based on
timestamps. The buffer should persist when you exit/launch the watchface, so you don't
lose the graph.

| Bytes | Field         | Type      | Description                                     | Unit      |
|-------|---------------|-----------|-------------------------------------------------|-----------|
| 4     | ref_timestamp | uint32    | Unix epoch time of the reference (oldest) point | seconds   |
| 2     | count         | uint16    | Number of points, N                             |           |
| 2N    | offsets       | uint16[N] | Time of each point since `ref_timestamp`        | minutes   |
| N     | bg_values     | uint8[N]  | BG of each point                                | mg/dL / 2 |

Little-endian. `bg_values` are mg/dL / 2, which fits 0–510 mg/dL (0–28 mmol/L) at 2 mg/dL
(≈0.1 mmol/L) resolution in one byte.

Total size: `6 + 3N` bytes (3 hours at 5 min intervals = 114 bytes).

## Message keys: Bitmap graph (sender 🡒 watchface)

This section is reserved for bitmap graph support, as an alternative to the raw graph. The xDrip-Pebble integration has had graph support for many years, using a PNG image rendered in xDrip and sent to the watchface.

| Key   | Name | Type | Description |
|-------|------|------|-------------|
| 40-49 |      |      | *Reserved*  |

## Implementation notes

* Use raw integer keys in watchfaces, don't declare messageKeys in package.json.
* BG timestamp should advance on new BG readings even if the BG is the same.
* Watchfaces with a BG graph can use ether a pre-rendered bitmap, or receive raw data to render itself.
* Use Clay or equivalent if your watchface needs user config.
* See e.g. [this](https://github.com/mortenfyhn/pebble-glucose-watchface) for an example watchface implementation.
