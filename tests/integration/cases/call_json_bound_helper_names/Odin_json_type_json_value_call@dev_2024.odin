#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
arena := _json_parse(`{"a": 1}`)
ZVal := _json_parse(`{"a": 1}`)
ZKV := _json_parse(`{"a": 1}`)
process(arena);
process(ZVal);
process(ZKV);
}
