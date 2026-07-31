# Pebble Glucose Protocol

A small AppMessage protocol for pushing glucose data to a Pebble watchface, so that watchfaces and data
sources (such as xDrip) can be developed independently of each other.

**[The spec is here →](PEBBLE_GLUCOSE_PROTOCOL.md)**

## Status

Draft of v1. Three implementations built and in daily use: a [watchface](https://github.com/mortenfyhn/pebble-glucose-watchface), a [bridge app](https://github.com/mortenfyhn/minimed-pebble-bridge) reading a pump over BLE, and a [modified PebbleOS](https://github.com/mortenfyhn/PebbleOS) reading the pump directly from the watch.

## Using it

Copy [`protocol.h`](protocol.h) into your project.

## License

[Zero-Clause BSD](https://opensource.org/license/0bsd): You can do anything you want, no attribution needed.
