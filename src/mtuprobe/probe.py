from collections import Callable


def bisect(n, mapper, tester):
    """
    Runs a bisection.

    - `n` is the number of elements to be bisected
    - `mapper` is a callable that will transform an integer from "0" to "n"
      into a value that can be tested
    - `tester` returns true if the value is within the "right" range
    """

    if n < 1:
        raise ValueError("Cannot bisect an empty array")

    left = 0
    right = n - 1

    while left + 1 < right:
        mid = int((left + right) / 2)

        val = mapper(mid)

        if tester(val):
            right = mid
        else:
            left = mid

    return mapper(right)


def probe_mtu(
    bin_path: str, addr: str, count: int, max_size: int, quiet: bool, runner: Callable
) -> None:
    """
    Uses a bisection algorithm to pinpoint the exact MTU of the path

    Parameters
    ----------
    bin_path
        Path to the ping binary
    addr
        Address to ping
    count
        Number of pings to do for each try
    max_size
        Max MTU size to test
    quiet
        Stay quiet in the output (just print the found MTU)
    runner
        Ping runner function
    """

    def mapper(n):
        return n + 1

    def tester(n):
        if not quiet:
            print(f"\rTesting packet size: {n: >6}", end="", flush=True)

        return not runner(
            bin_path=bin_path,
            addr=addr,
            count=count,
            size=n,
        )

    size = bisect(max_size, mapper, tester) - 1

    if not quiet:
        extra = 8 + 20  # ICMP + IPv4

        print(f"\rMax packet size:       {size: >6}")
        print(f"Expected ethernet MTU: {size + extra: >6}")
    else:
        print(f"{size}")
