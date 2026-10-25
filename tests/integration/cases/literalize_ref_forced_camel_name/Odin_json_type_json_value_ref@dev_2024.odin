#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
userObj := _json_parse(`{"_": "_"}`)
my_data := _json_parse(`{"$ref": "USER_OBJ"}`)
_ = my_data
}
