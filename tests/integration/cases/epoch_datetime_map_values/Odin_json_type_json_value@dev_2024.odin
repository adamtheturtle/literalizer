#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
my_data := _json_parse(`{"within_i32": "2024-01-15T12:00:00Z", "beyond_i32": "2099-06-15T08:30:00Z"}`)
_ = my_data
}
