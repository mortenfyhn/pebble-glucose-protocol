# Pebble Glucose Protocol

An open AppMessage protocol for sending glucose/CGM data to Pebble watches, so that watchfaces and data
sources (like xDrip) can be developed independently.

👉 **[Protocol spec here](PROTOCOL.md)** 👈

<img width="400" alt="Image" src="https://github.com/user-attachments/assets/40408378-5ce9-42ae-88d2-50b169ceb74b" />

## Using it

Copy any of these into your project:

* [`protocol.h`](protocol.h) for C projects
* [`Protocol.kt`](Protocol.kt) for Kotlin projects
* or port it to your language

## Status

This is a v1 draft. I have three implementations in daily use:

* [Pebble watchface](https://github.com/mortenfyhn/pebble-glucose-watchface)
* [Android bridge app](https://github.com/mortenfyhn/minimed-pebble-bridge), to read my pump/CGM and forward to the watch
* [PebbleOS fork](https://github.com/mortenfyhn/PebbleOS), to read the pump directly from the watch (no phone between)

## License

[Zero-Clause BSD](https://opensource.org/license/0bsd): You can do anything you want, and you don't have to credit anyone.
