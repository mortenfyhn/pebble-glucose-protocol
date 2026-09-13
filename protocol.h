// Pebble Glucose Protocol
//
// Generated from PROTOCOL.md (639658c). Do not edit directly.

#pragma once

#define PROTOCOL_VERSION 1

// Message keys: Watchface -> sender (capability announcement)
#define KEY_PROTOCOL_VERSION 0 // Protocol version (increment for breaking changes)
#define KEY_CAPABILITIES 1 // Watchface capability bitfield, see below
#define KEY_GRAPH_HOURS 2 // Hours of graph history, set 0 to disable
// Keys 3-9 reserved

// Message keys: Sender -> watchface (data)
#define KEY_BG_TIMESTAMP 10 // BG reading timestamp (Unix epoch seconds)
#define KEY_BG_STRING 11 // Formatted BG value in sender's units (e.g. "5.7" or "103")
#define KEY_DELTA_STRING 12 // Formatted BG delta (e.g. "-0.3" or "-5.6")
#define KEY_TREND_ARROW 13 // Trend arrow index (see below)
#define KEY_IOB_STRING 14 // Formatted insulin-on-board (e.g. "2.5")
#define KEY_STATUS_STRING 15 // Any sensor/pump status text (e.g. "PUMP SUSPENDED")
#define KEY_SENDER_BATTERY 16 // Sender battery level (0–100)
#define KEY_STATUS_START 17 // Start time of current status, can be used to display a count-up timer (Unix epoch seconds)
#define KEY_STATUS_END 18 // End time of current status, can be used to display a count-down timer (Unix epoch seconds)
// Keys 19-29 reserved

// Message keys: Sender -> watchface (raw graph)
#define KEY_GRAPH_DATA 30 // Raw graph data, see below
#define KEY_GRAPH_HIGH_LINE 31 // High BG threshold (mg/dL / 2)
#define KEY_GRAPH_LOW_LINE 32 // Low BG threshold (mg/dL / 2)
// Keys 33-39 reserved

// Keys 40-49 reserved for bitmap graph

// Capability bits
#define CAP_BG 0x01 // Timestamped BG value
#define CAP_TREND_ARROW 0x02 // Trend arrow
#define CAP_DELTA 0x04 // Delta
#define CAP_IOB 0x08 // Insulin-on-board
#define CAP_STATUS 0x10 // Status line
#define CAP_SENDER_BATTERY 0x20 // Sender battery

// Trend arrow indices
#define TREND_UNKNOWN 0 // Unknown
#define TREND_FLAT 1 // Flat
#define TREND_SLANT_UP 2 // Slant up
#define TREND_SLANT_DOWN 3 // Slant down
#define TREND_UP 4 // Up
#define TREND_DOWN 5 // Down
#define TREND_DOUBLE_UP 6 // Double up
#define TREND_DOUBLE_DOWN 7 // Double down
#define TREND_TRIPLE_UP 8 // Triple up
#define TREND_TRIPLE_DOWN 9 // Triple down
