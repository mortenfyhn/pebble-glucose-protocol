// Pebble Glucose Protocol
//
// Generated from PROTOCOL.md (639658c). Do not edit directly.

object Protocol {
    const val PROTOCOL_VERSION = 1

    // Keys are UInt because that is what PebbleKit Android 2 dictionaries take.

    // Message keys: Watchface -> sender (capability announcement)
    const val KEY_PROTOCOL_VERSION: UInt = 0u // Protocol version (increment for breaking changes)
    const val KEY_CAPABILITIES: UInt = 1u // Watchface capability bitfield, see below
    const val KEY_GRAPH_HOURS: UInt = 2u // Hours of graph history, set 0 to disable
    // Keys 3-9 reserved

    // Message keys: Sender -> watchface (data)
    const val KEY_BG_TIMESTAMP: UInt = 10u // BG reading timestamp (Unix epoch seconds)
    const val KEY_BG_STRING: UInt = 11u // Formatted BG value in sender's units (e.g. "5.7" or "103")
    const val KEY_DELTA_STRING: UInt = 12u // Formatted BG delta (e.g. "-0.3" or "-5.6")
    const val KEY_TREND_ARROW: UInt = 13u // Trend arrow index (see below)
    const val KEY_IOB_STRING: UInt = 14u // Formatted insulin-on-board (e.g. "2.5")
    const val KEY_STATUS_STRING: UInt = 15u // Any sensor/pump status text (e.g. "PUMP SUSPENDED")
    const val KEY_SENDER_BATTERY: UInt = 16u // Sender battery level (0–100)
    const val KEY_STATUS_START: UInt = 17u // Start time of current status, can be used to display a count-up timer (Unix epoch seconds)
    const val KEY_STATUS_END: UInt = 18u // End time of current status, can be used to display a count-down timer (Unix epoch seconds)
    // Keys 19-29 reserved

    // Message keys: Sender -> watchface (raw graph)
    const val KEY_GRAPH_DATA: UInt = 30u // Raw graph data, see below
    const val KEY_GRAPH_HIGH_LINE: UInt = 31u // High BG threshold (mg/dL / 2)
    const val KEY_GRAPH_LOW_LINE: UInt = 32u // Low BG threshold (mg/dL / 2)
    // Keys 33-39 reserved

    // Keys 40-49 reserved for bitmap graph

    // Capability bits
    const val CAP_BG = 0x01 // Timestamped BG value
    const val CAP_TREND_ARROW = 0x02 // Trend arrow
    const val CAP_DELTA = 0x04 // Delta
    const val CAP_IOB = 0x08 // Insulin-on-board
    const val CAP_STATUS = 0x10 // Status line
    const val CAP_SENDER_BATTERY = 0x20 // Sender battery

    // Trend arrow indices
    const val TREND_UNKNOWN = 0 // Unknown
    const val TREND_FLAT = 1 // Flat
    const val TREND_SLANT_UP = 2 // Slant up
    const val TREND_SLANT_DOWN = 3 // Slant down
    const val TREND_UP = 4 // Up
    const val TREND_DOWN = 5 // Down
    const val TREND_DOUBLE_UP = 6 // Double up
    const val TREND_DOUBLE_DOWN = 7 // Double down
    const val TREND_TRIPLE_UP = 8 // Triple up
    const val TREND_TRIPLE_DOWN = 9 // Triple down
}
