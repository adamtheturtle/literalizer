#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
my_data := _json_parse(`{"quote\"backslash\\": 1, "line\nbreak": 2, "$(literal)${text}": 3, "RStr prefix": 4}`)
_ = my_data
}
