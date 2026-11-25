#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
my_data := _json_parse(`{"morning": "09:30:00", "afternoon": "14:15:00", "evening": "23:59:59"}`)
_ = my_data
}
