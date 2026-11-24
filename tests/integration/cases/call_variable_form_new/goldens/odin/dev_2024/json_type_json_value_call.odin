#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := make_widget(_json_parse(`42`))
_ = my_data
}
