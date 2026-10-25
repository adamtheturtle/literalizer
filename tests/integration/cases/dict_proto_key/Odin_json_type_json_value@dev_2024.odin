#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
my_data := _json_parse(`{"__proto__": {"x": 1}, "n": {"__proto__": 3}, "y": 2}`)
_ = my_data
}
