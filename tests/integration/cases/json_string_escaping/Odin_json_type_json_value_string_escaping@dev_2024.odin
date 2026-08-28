#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
my_data := _json_parse(`{"$key": "a\"b\tcé #{world} $ident", "trailing multi-byte": "café"}`)
_ = my_data
}
