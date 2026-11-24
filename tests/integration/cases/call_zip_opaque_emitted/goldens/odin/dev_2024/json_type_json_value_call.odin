#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}
process :: proc(args: ..any) -> any { return nil }
emit :: proc(args: ..any) -> any { return nil }

main :: proc() {
emit(process(_json_parse(`1`)), _json_parse(`"2024-01-15T12:00:00Z"`));
}
