#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
my_data := _json_parse(`["This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.", 1]`)
_ = my_data
}
