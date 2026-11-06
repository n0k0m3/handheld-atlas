#!/usr/bin/env python3
"""Serve the built site locally the way surge.sh serves it.

Usage:
    uv run serve.py [--port 8765] [--bind 127.0.0.1] [--dir ../site/dist]

surge.sh answers /<name> with <name>.html, redirects /<name>/ to /<name>,
and answers any other path with no file with 200.html. This server does the
same. In site/dist (no 200.html) the fallback is index.html, so a reload on
any screen works. `python -m http.server` returns 404 there.

To test the pages build, write it to a folder and serve that folder:
    uv run build_site.py --pages /tmp/pages --site-url http://127.0.0.1:8765
    uv run serve.py --dir /tmp/pages
"""
import argparse
import functools
import http.server
import pathlib
import sys

DIST = pathlib.Path(__file__).resolve().parent.parent / "site" / "dist"


class Handler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        url, _, query = self.path.partition("?")
        query = "?" + query if query else ""
        root = pathlib.Path(self.directory)
        if url == "/":
            self.path = "/index.html" + query
            return super().send_head()
        if pathlib.Path(self.translate_path(url)).is_file():
            return super().send_head()
        if url.endswith("/"):
            self.send_response(301)
            self.send_header("Location", url.rstrip("/") + query)
            self.end_headers()
            return None
        if pathlib.Path(self.translate_path(url + ".html")).is_file():
            self.path = url + ".html" + query
            return super().send_head()
        self.path = ("/200.html" if (root / "200.html").is_file() else "/index.html") + query
        return super().send_head()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--bind", default="127.0.0.1")
    ap.add_argument("--dir", type=pathlib.Path, default=DIST, help="folder to serve (default: site/dist)")
    args = ap.parse_args(argv)
    root = args.dir.resolve()
    if not (root / "index.html").is_file():
        print(f"ERROR {root}/index.html is missing. Run build_site.py first.")
        return 1
    handler = functools.partial(Handler, directory=str(root))
    with http.server.ThreadingHTTPServer((args.bind, args.port), handler) as srv:
        print(f"Serving {root} at http://{args.bind}:{args.port}/")
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
