from subprocess import DEVNULL, Popen
from sys import stderr


def auto(bin_path: str, addr: str, count: int, size: int) -> bool:
    """
    In the future, auto-detect which ping implementation to call, however for
    now just forwards the call to gnu.

    Returns True if at least one ping went through (and came back)

    Parameters
    ----------
    bin_path
        Path to ping binary
    addr
        Address to ping
    count
        Number of pings to send
    size
        Size of the payload
    """

    return gnu(bin_path, addr, count, size)


def gnu(bin_path: str, addr: str, count: int, size: int) -> bool:
    """
    Using the GNU ping (so Linux machines most likely)
    """

    try:
        with Popen(
            args=[
                bin_path,
                "-i",
                "0.2",
                "-c",
                f"{count}",
                "-M",
                "do",
                "-s",
                f"{size}",
                addr,
            ],
            stdout=DEVNULL,
            stdin=DEVNULL,
            stderr=DEVNULL,
        ) as p:
            p.wait()
    except FileNotFoundError:
        stderr.write(f'\rping binary "{bin_path}" could not be found\n')
        stderr.flush()
        exit(1)
    except PermissionError:
        stderr.write(f'\rping binary "{bin_path}" cannot be executed\n')
        stderr.flush()
        exit(1)

    return not p.returncode
