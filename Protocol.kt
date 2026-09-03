// Pebble Glucose Protocol
//
// Copy this file into your sender project and add your own `package` line.
// Kotlin mirror of protocol.h.
//
// See PROTOCOL.md for all definitions.

object Protocol {
    const val PROTOCOL_VERSION = 1 // draft!

    // Keys are UInt because that is what PebbleKit Android 2 dictionaries take.

    // Message keys: Watchface -> sender (capability announcement)
    const val KEY_PROTOCOL_VERSION: UInt = 0u
    const val KEY_CAPABILITIES: UInt = 1u
    const val KEY_GRAPH_HOURS: UInt = 2u
    // Keys 3-9 reserved

    // Message keys: Sender -> watchface (data)
    const val KEY_BG_TIMESTAMP: UInt = 10u
    const val KEY_BG_STRING: UInt = 11u
    const val KEY_DELTA_STRING: UInt = 12u
    const val KEY_TREND_ARROW: UInt = 13u
    const val KEY_IOB_STRING: UInt = 14u
    const val KEY_STATUS_STRING: UInt = 15u
    const val KEY_SENDER_BATTERY: UInt = 16u
    // Keys 17-29 reserved

    // Message keys: Sender -> watchface (raw graph)
    const val KEY_GRAPH_DATA: UInt = 30u
    const val KEY_GRAPH_HIGH_LINE: UInt = 31u
    const val KEY_GRAPH_LOW_LINE: UInt = 32u
    // Keys 33-39 reserved

    // Keys 40-49 reserved for bitmap graph

    // Capability bits
    const val CAP_BG = 1 shl 0
    const val CAP_TREND_ARROW = 1 shl 1
    const val CAP_DELTA = 1 shl 2
    const val CAP_IOB = 1 shl 3
    const val CAP_STATUS = 1 shl 4
    const val CAP_SENDER_BATTERY = 1 shl 5

    // Trend arrow indices
    const val TREND_UNKNOWN = 0
    const val TREND_FLAT = 1
    const val TREND_SLANT_UP = 2
    const val TREND_SLANT_DOWN = 3
    const val TREND_UP = 4
    const val TREND_DOWN = 5
    const val TREND_DOUBLE_UP = 6
    const val TREND_DOUBLE_DOWN = 7
    const val TREND_TRIPLE_UP = 8
    const val TREND_TRIPLE_DOWN = 9
}
