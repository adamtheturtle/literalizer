#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
my_data := _json_parse(`{"date": "0099-05-27", "naive": "0001-01-01T12:30:00Z", "recent": "2024-05-27T10:00:00Z"}`)
_ = my_data
}
