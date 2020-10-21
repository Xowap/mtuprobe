from argparse import ArgumentParser
from enum import Enum
from typing import Optional, Sequence

from . import ping
from .probe import probe_mtu


class Mode(Enum):
    """
    Ping compatibility mode

    - auto = auto-detect
    - gnu = GNU ping implementation
    """

    auto = "auto"
    gnu = "gnu"


def positive_int(i) -> int:
    """
    Checks that provided integers are positive and non-null (from CLI args)

    Parameters
    ----------
    i
        String to parse
    """

    x = int(i)

    if x <= 0:
        raise ValueError("Integer must be postitive and non-null")

    return x


def parse_args(argv: Optional[Sequence[str]] = None):
    """
    Setups and executes the CLI arguments parser

    Parameters
    ----------
    argv
        If not specified, argparse will default to the "real" argv
    """

    parser = ArgumentParser(
        description=(
            "mtuprobe uses the system ping utility to determine the IPv4 MTU "
            "between current machine and a network address"
        )
    )

    parser.add_argument(
        "-b", "--ping-bin", default="ping", help="Path to ping binary (default: ping)"
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=Mode,
        default=Mode.auto,
        help=(
            "Compatibility mode of the binary. Options: "
            + ", ".join([x.name for x in Mode])
            + ". (default: auto)"
        ),
    )
    parser.add_argument(
        "-s",
        "--max-size",
        type=positive_int,
        help="Max payload size (default: 3000)",
        default=3000,
    )
    parser.add_argument(
        "-c",
        "--count",
        default=4,
        type=positive_int,
        help="Number of pings sent (default: 4)",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="If set, only the MTU will be printed",
    )

    parser.add_argument("address", help="Address you want to ping")

    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None):
    """
    Executes the main program

    Parameters
    ----------
    argv
        Provide custom CLI args if you call this from Python, otherwise the
        "real ones" will be used
    """

    args = parse_args(argv)
    probe_mtu(
        bin_path=args.ping_bin,
        addr=args.address,
        count=args.count,
        max_size=args.max_size,
        quiet=args.quiet,
        runner=getattr(ping, args.mode.name),
    )


def __main__():
    """
    Wrapper around the main function to catch interrupts
    """

    try:
        main()
    except KeyboardInterrupt:
        pass
    except SystemExit:
        pass


if __name__ == "__main__":
    __main__()
