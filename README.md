# Pebble Glucose Protocol

A small AppMessage protocol for pushing glucose data to a Pebble watchface, so that watchfaces and data
sources (such as xDrip) can be developed independently.

👉 **[Protocol spec here](PROTOCOL.md)** 👈

## Using it

Copy any of these into your project:
* [`protocol.h`](protocol.h) for C projects
* [`Protocol.kt`](Protocol.kt) for Kotlin projects

## Status

This is a v1 draft. I have three implementations in daily use:
* [Pebble watchface](https://github.com/mortenfyhn/pebble-glucose-watchface)
* [Android bridge app](https://github.com/mortenfyhn/minimed-pebble-bridge), to read my pump/CGM and forward to the watch
* [PebbleOS fork](https://github.com/mortenfyhn/PebbleOS), to read the pump directly from the watch (no phone between)

Example watchface:

<img height="400" alt="Image" src="https://github.com/user-attachments/assets/40408378-5ce9-42ae-88d2-50b169ceb74b" />

## License

[Zero-Clause BSD](https://opensource.org/license/0bsd): You can do anything you want, and you don't have to credit anyone.
