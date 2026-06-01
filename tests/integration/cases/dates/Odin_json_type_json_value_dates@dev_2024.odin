#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
my_data := _json_parse(`{"date": "2024-01-15", "datetime": "2024-01-15T12:30:00+00:00"}`)
_ = my_data
}
