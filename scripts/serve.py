#!/usr/bin/env python3
"""Serve site/dist locally the way surge.sh serves the site.

Usage:
    uv run serve.py [--port 8765] [--bind 127.0.0.1]

surge.sh answers a path with no file (/browse, /compare?d=..., /<device-id>)
with 200.html, a copy of index.html. This server answers such a path with
index.html, so a reload on any screen works. `python -m http.server` returns
404 there.
"""
import argparse
import functools
import http.server
import pathlib
import sys

DIST = pathlib.Path(__file__).resolve().parent.parent / "site" / "dist"


class Handler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = pathlib.Path(self.translate_path(self.path))
        if not path.is_file():
            self.path = "/index.html"
        return super().send_head()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--bind", default="127.0.0.1")
    args = ap.parse_args(argv)
    if not (DIST / "index.html").is_file():
        print("ERROR site/dist/index.html is missing. Run build_site.py first.")
        return 1
    handler = functools.partial(Handler, directory=str(DIST))
    with http.server.ThreadingHTTPServer((args.bind, args.port), handler) as srv:
        print(f"Serving {DIST} at http://{args.bind}:{args.port}/")
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
