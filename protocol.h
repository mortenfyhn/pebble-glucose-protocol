// Pebble Glucose Protocol v1 — full key and capability set.
//
// See PEBBLE_GLUCOSE_PROTOCOL.md for what each field means and how the exchange works.
//
// Copy this file into your project. It is header-only and has no dependencies; there is nothing to
// build or link. Key numbers are frozen once published (see "Key stability" in the spec), so a copy
// can fall behind but cannot silently disagree.
//
// Use these numbers directly with dict_find() — do NOT declare messageKeys in package.json. The SDK
// assigns those automatically, which cannot work for numbers fixed across independently-released apps.
//
// A watchface only needs the keys it actually implements; unused defines cost nothing, so copying the
// whole file is fine. Trimming it to a curated subset is also fine, and doubles as documentation of
// what your face supports.

#pragma once

// Bump only for breaking changes. Adding fields is not breaking.
#define PROTOCOL_VERSION 1

// ---------------------------------------------------------------------------
// Watch -> sender: capability announcement
//
// Sent on launch and on every Bluetooth reconnect. The sender replies with an immediate push of the
// requested fields, even if nothing has changed.
// ---------------------------------------------------------------------------

#define KEY_PROTOCOL_VERSION 0 // uint8
#define KEY_CAPABILITIES 1     // uint32, bitfield of CAP_* below
#define KEY_GRAPH_HOURS 2      // uint8, widest graph window this face can show, in hours; 0 = no graph

// #define KEY_GRAPH_BITMAP_SIZE 3  // RESERVED — sender-rendered bitmap geometry, unspecified

// ---------------------------------------------------------------------------
// Sender -> watch: current reading
// ---------------------------------------------------------------------------

#define KEY_BG_TIMESTAMP 10   // uint32, UNIX epoch seconds of the reading itself
#define KEY_BG_STRING 11      // string, pre-formatted in the sender's units, e.g. "7.5" or "135"
#define KEY_DELTA_STRING 12   // string, pre-formatted change since previous reading, e.g. "+0.3"
#define KEY_TREND_ARROW 13    // uint8, TREND_* below
#define KEY_IOB_STRING 14     // string, pre-formatted insulin-on-board, e.g. "2.5"
#define KEY_STATUS_STRING 15  // string, status line e.g. "SUSPENDED"; "" = nothing to show
#define KEY_SENDER_BATTERY 16 // uint8, 0-100

// ---------------------------------------------------------------------------
// Sender -> watch: graph
//
// KEY_GRAPH_HOURS (2) is echoed back with the active window, which may be narrower than the
// watchface asked for. Use it as the time axis directly rather than inferring the span from the data.
// ---------------------------------------------------------------------------

#define KEY_GRAPH_DATA 17      // bytes: [ref_ts u32][count u16][offset_min u16 xN][bg u8 xN], LE
#define KEY_GRAPH_HIGH_LINE 18 // uint8, high target line, mg/dL / 2 (90 = 180 mg/dL = 10.0 mmol/L)
#define KEY_GRAPH_LOW_LINE 19  // uint8, low target line, mg/dL / 2 (36 = 72 mg/dL = 4.0 mmol/L)

// #define KEY_GRAPH_BITMAP 20  // RESERVED — sender-rendered bitmap, chunked, unspecified

// ---------------------------------------------------------------------------
// Capability bits, for KEY_CAPABILITIES
//
// The graph is requested via KEY_GRAPH_HOURS rather than a bit, since it needs a window anyway.
// ---------------------------------------------------------------------------

#define CAP_BG (1 << 0)             // BG value + timestamp
#define CAP_TREND_ARROW (1 << 1)
#define CAP_DELTA (1 << 2)
#define CAP_IOB (1 << 3)
#define CAP_STATUS (1 << 4)
#define CAP_SENDER_BATTERY (1 << 5)
// #define CAP_GRAPH_BITMAP (1 << 6)  // RESERVED — may not be needed, see spec

// ---------------------------------------------------------------------------
// Trend arrow indices, for KEY_TREND_ARROW
// ---------------------------------------------------------------------------

#define TREND_UNKNOWN 0
#define TREND_FLAT 1
#define TREND_SLANT_UP 2
#define TREND_SLANT_DOWN 3
#define TREND_UP 4
#define TREND_DOWN 5
#define TREND_DOUBLE_UP 6
#define TREND_DOUBLE_DOWN 7
#define TREND_TRIPLE_UP 8
#define TREND_TRIPLE_DOWN 9
