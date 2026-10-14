#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
shared := _json_parse(`null`)
consume(_json_parse(`{"left": {"$ref": "shared"}, "nested": [{"$ref": "shared"}]}`));
}
