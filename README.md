mtuprobe
========

A tool to probe the current
[MTU](https://en.wikipedia.org/wiki/Maximum_transmission_unit) on an IPv4 path.

So far it's compatible with Linux only however it can very easily be adapted
to any other operating system.

## Installation

```
pip install mtuprobe
```

## Usage

The default options are sane and should give you good results. Suppose that
you want to know the current effective MTU towards `wikipedia.org`, in a shell
you can try:

```
% mtuprobe wikipedia.org
Max packet size:         1464
Expected ethernet MTU:   1492
```

You can check out `mtuprobe -h` to get the complete list of options.

Values are:

- **Max packet size** &mdash; Max packet size specified to `ping`, meaning the
  size of the data segment of the ICMP packet
- **Expected ethernet MTU** &mdash; That's what the MTU should be if you're
  transmitting over Ethernet and the header sizes are what is expected from
  such a setup. This should apply most of the time but surely some weird
  network setups could violate this.
