#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
shared := _json_parse(`[1, 2]`)
my_data := _json_parse(`{"$ref": "shared"}`)
consume_widget(my_data);
}
