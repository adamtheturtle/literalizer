#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
my_data := _json_parse(`["1901-12-13T20:45:51Z", "1901-12-13T20:45:52Z", "2038-01-19T03:14:07Z", "2038-01-19T03:14:08Z"]`)
_ = my_data
}
