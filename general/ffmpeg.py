#!/usr/bin/env python3
"""Simple ffmpeg helper script for converting webm to mp4 and merging mp4 files."""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path
import shutil

if shutil.which("ffmpeg") is None:
    sys.exit("Error: ffmpeg is not installed or not in PATH.")

def convert(args):
    """Convert a webm file to mp4."""
    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Error: input file '{input_path}' does not exist.")

    output = args.output or input_path.with_suffix(".mp4").name
    cmd = ["ffmpeg", "-i", str(input_path), "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", output]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def merge(args):
    """Merge two or more mp4 files together."""
    for f in args.inputs:
        if not Path(f).exists():
            raise FileNotFoundError(f"Error: input file '{f}' does not exist.")

    output = args.output or "output.mp4"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
        for f in args.inputs:
            tmp.write(f"file '{Path(f).resolve()}'\n")
        tmp_path = tmp.name

    try:
        cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", tmp_path, "-c", "copy", output]
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(
        description="ffmpeg helper utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  %(prog)s convert recording.webm
  %(prog)s convert recording.webm -o my-video.mp4
  %(prog)s merge first.mp4 second.mp4
  %(prog)s merge clip1.mp4 clip2.mp4 clip3.mp4 -o combined.mp4
""",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # convert subcommand
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert a webm file to mp4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Convert a .webm file to .mp4 using ffmpeg (video stream copied, audio re-encoded to AAC 128k).",
        epilog="""\
examples:
  %(prog)s recording.webm
  %(prog)s recording.webm -o my-video.mp4
""",
    )
    convert_parser.add_argument("input", help="Input webm file")
    convert_parser.add_argument("-o", "--output", help="Output mp4 file (default: <input>.mp4)")

    # merge subcommand
    merge_parser = subparsers.add_parser(
        "merge",
        help="Merge two or more mp4 files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Merge (concatenate) two or more .mp4 files into a single file. The order of inputs matters.",
        epilog="""\
examples:
  %(prog)s first.mp4 second.mp4
  %(prog)s clip1.mp4 clip2.mp4 clip3.mp4 -o combined.mp4
""",
    )
    merge_parser.add_argument("inputs", nargs="+", help="Input mp4 files to merge (order matters)")
    merge_parser.add_argument("-o", "--output", help="Output mp4 file (default: output.mp4)")

    args = parser.parse_args()

    if args.command == "convert":
        convert(args)
        return
    if args.command == "merge":
        merge(args)
        return


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(f"Error: {e}")
