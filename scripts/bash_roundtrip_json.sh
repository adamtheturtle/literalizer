# shellcheck shell=bash

# A minimal JSON string escaper: the round-trip must serialize the
# *runtime* value, so escaping happens in Bash rather than being baked
# in at code-generation time.  Backslash is replaced first so the
# escapes added afterwards are not doubled.  Every C0 control is
# covered, not just the five with short escapes, because JSON forbids
# all of them raw (issue #4545).  DEL and the C1 range are legal in a
# JSON string without an escape and pass through as UTF-8 bytes do.
_json_str() {
    local s=$1
    s=${s//\\/\\\\}
    s=${s//\"/\\\"}
    s=${s//$'\x00'/\\u0000}
    s=${s//$'\x01'/\\u0001}
    s=${s//$'\x02'/\\u0002}
    s=${s//$'\x03'/\\u0003}
    s=${s//$'\x04'/\\u0004}
    s=${s//$'\x05'/\\u0005}
    s=${s//$'\x06'/\\u0006}
    s=${s//$'\x07'/\\u0007}
    s=${s//$'\x08'/\\b}
    s=${s//$'\x09'/\\t}
    s=${s//$'\x0a'/\\n}
    s=${s//$'\x0b'/\\u000b}
    s=${s//$'\x0c'/\\f}
    s=${s//$'\x0d'/\\r}
    s=${s//$'\x0e'/\\u000e}
    s=${s//$'\x0f'/\\u000f}
    s=${s//$'\x10'/\\u0010}
    s=${s//$'\x11'/\\u0011}
    s=${s//$'\x12'/\\u0012}
    s=${s//$'\x13'/\\u0013}
    s=${s//$'\x14'/\\u0014}
    s=${s//$'\x15'/\\u0015}
    s=${s//$'\x16'/\\u0016}
    s=${s//$'\x17'/\\u0017}
    s=${s//$'\x18'/\\u0018}
    s=${s//$'\x19'/\\u0019}
    s=${s//$'\x1a'/\\u001a}
    s=${s//$'\x1b'/\\u001b}
    s=${s//$'\x1c'/\\u001c}
    s=${s//$'\x1d'/\\u001d}
    s=${s//$'\x1e'/\\u001e}
    s=${s//$'\x1f'/\\u001f}
    printf '"%s"' "$s"
}
