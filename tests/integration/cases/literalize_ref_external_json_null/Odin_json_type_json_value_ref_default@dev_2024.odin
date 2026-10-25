#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}
consume_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
item := _json_parse(`null`)
my_data := _json_parse(`null`)
consume_widget(my_data);
my_data = _json_parse(`{"$ref": "item"}`)
consume_widget(my_data);
}
