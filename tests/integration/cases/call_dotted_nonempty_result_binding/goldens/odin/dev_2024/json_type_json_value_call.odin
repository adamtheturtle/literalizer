#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}
_thing_go_ :: proc(args: ..any) -> any { return nil }
ThingType_ :: struct { go: proc(..any) -> any }

main :: proc() {
thing: ThingType_ = ThingType_{ go = _thing_go_ }
my_data := thing.go(_json_parse(`[1]`))
_ = my_data
}
