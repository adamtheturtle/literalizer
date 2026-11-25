#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
my_data := _json_parse(`[5e-324, -5e-324, 1e-310]`)
_ = my_data
}
