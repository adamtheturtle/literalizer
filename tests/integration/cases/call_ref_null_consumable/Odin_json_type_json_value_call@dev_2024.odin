#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_null := _json_parse(`null`)
regular_null := _json_parse(`null`)
consume(my_null);
consume(regular_null);
}
