#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}
make_widget :: proc(args: ..any) -> any { return nil }
consume :: proc(args: ..any) -> any { return nil }

main :: proc() {
my_data := make_widget(_json_parse(`7`))
consume(my_data);
my_data = (make_widget(_json_parse(`13`)) != nil ?
make_widget(_json_parse(`13`)) \
 // inner
: nil) // trailing
consume(my_data);
}
