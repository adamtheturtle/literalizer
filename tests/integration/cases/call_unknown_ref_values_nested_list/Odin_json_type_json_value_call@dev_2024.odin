#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}
process :: proc(args: ..any) -> any { return nil }

main :: proc() {
unknown_value := _json_parse(`[]`)
process(_json_parse(`[{"$ref": "unknown_value"}]`));
}
