#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
my_data := _json_parse(`["C:\\path\\to\\file", "back\\\\slash", "hello \\\"world\\\"", "path\\to \"# file", "trailing\\", "both \"quotes''' here", "line1\\nline2\nwith newline"]`)
_ = my_data
}
