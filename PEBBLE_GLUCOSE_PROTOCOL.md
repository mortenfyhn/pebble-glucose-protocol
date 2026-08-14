# Pebble Glucose Protocol

**Draft of Version 1**

This is a suggested protocol for sending glucose/CGM data to a Pebble watchface over [AppMessage](https://developer.rebble.io/). It decouples the watchface from the data source.

- Sender: Anything with glucose data and a Pebble link (xDrip, a custom app, or something else).
- Watchface: Any Pebble watchface implementing this protocol.

Each watchface has a UUID, which the sender must target. To support arbitrary watchfaces the sender must let the user set the watchface UUID.

## Communication flow

1. On launch and reconnect, the watchface sends a capability announcement
2. The sender stores the capabilities and responds with the corresponding data
3. The sender sends new data when it has any.
4. The watchface can re-send its announcement any time to request a full refresh.

## Message keys: Capability announcement (watchface 🡒 sender)

| Key | Name              | Type   | Description |
|-----|-------------------|--------|-------------|
| 0   | PROTOCOL_VERSION  | uint8  | Protocol version (increment for breaking changes) |
| 1   | CAPABILITIES      | uint32 | Watchface capability bitfield, see below |
| 2   | GRAPH_HOURS       | uint8  | Hours of graph history, set 0 to disable |
| 3   | GRAPH_BITMAP_SIZE |        | *Reserved for pre-rendered bitmap graph* |
| 4-9 |                   |        | *Reserved* |

Watchfaces can re-send the announcement any time to request a full update from the sender.

Capability bits:

| Bit | Mask   | Description |
|-----|--------|-------------|
| 0   | `0x01` | Timestamped BG value |
| 1   | `0x02` | Trend arrow |
| 2   | `0x04` | Delta |
| 3   | `0x08` | IOB |
| 4   | `0x10` | Status line |
| 5   | `0x20` | Sender battery |

## Message keys: Main data (sender 🡒 watchface)

| Key   | Name            | Type   | Description |
|-------|-----------------|--------|-------------|
| 10    | BG_TIMESTAMP    | uint32 | BG reading timestamp (Unix epoch seconds) |
| 11    | BG_STRING       | string | Formatted BG value in sender's units (e.g. "5.7" or "103") |
| 12    | DELTA_STRING    | string | Formatted BG delta (e.g. "-0.3" or "-5.6") |
| 13    | TREND_ARROW     | uint8  | Trend arrow index (see below) |
| 14    | IOB_STRING      | string | Formatted insulin-on-board (e.g. "2.5") |
| 15    | STATUS_STRING   | string | Any sensor/pump status text (e.g. "PUMP SUSPENDED") |
| 16    | SENDER_BATTERY  | uint8  | Sender battery level (0–100) |
| 17-29 |                 |        | *Reserved* |

Trend arrow indices:

| Index | Description |
|-------|-------------|
| 0     | Unknown     |
| 1     | Flat        |
| 2     | Slant up    |
| 3     | Slant down  |
| 4     | Up          |
| 5     | Down        |
| 6     | Double up   |
| 7     | Double down |
| 8     | Triple up   |
| 9     | Triple down |

## Message keys: Bitmap graph (sender 🡒 watchface)

| Key   | Name            | Type   | Description |
|-------|-----------------|--------|-------------|
| 30    | GRAPH_BITMAP    | bytes  | *Reserved for bitmap graph data* |
| 31-39 |                 |        | *Reserved* |

## Message keys: Raw graph (sender 🡒 watchface)

| Key   | Name            | Type   | Description |
|-------|-----------------|--------|-------------|
| 40    | GRAPH_DATA      | bytes  | Raw graph data, see below |
| 41    | GRAPH_HIGH_LINE | uint8  | High BG threshold (mg/dL / 2) |
| 42    | GRAPH_LOW_LINE  | uint8  | Low BG threshold (mg/dL / 2) |
| 43-49 |                 |        | *Reserved* |

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

Little-endian. `bg_values` are **mg/dL ÷ 2**, which fits 0–510 mg/dL (0–28 mmol/L) at 2 mg/dL
(≈0.1 mmol/L) resolution in one byte.

Total size: `6 + 3N` bytes (3 hours at 5 min intervals → 114 bytes).

## Implementation notes

* Use raw integer keys in watchfaces, don't declare messageKeys in package.json
* BG timestamp should advance on new BG readings even if the BG is the same
* Watchfaces with a BG graph can use ether a pre-rendered bitmap, or receive raw data to render itself
* Use Clay or equivalent if your watchface needs user config
* See e.g. [this](https://github.com/mortenfyhn/pebble-glucose-watchface) for an example watchface implementation
