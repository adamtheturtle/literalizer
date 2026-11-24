#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
// About a.
my_data := _json_parse(`{"a": 1, "b": 2}`)
_ = my_data
}
