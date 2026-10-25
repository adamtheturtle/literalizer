#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}

main :: proc() {
shared := _json_parse(`[1, 2]`)
build := _json_parse(`[1, 2]`)
json_object := _json_parse(`[1, 2]`)
json_allocator := _json_parse(`[1, 2]`)
json_entries := _json_parse(`[1, 2]`)
json_entry := _json_parse(`[1, 2]`)
my_data := _json_parse(`{"field": {"$ref": "shared"}, "nested": [{"$ref": "shared"}, {}], "build": {"$ref": "build"}, "json_object": {"$ref": "json_object"}, "json_allocator": {"$ref": "json_allocator"}, "json_entries": {"$ref": "json_entries"}, "json_entry": {"$ref": "json_entry"}}`)
_ = my_data
}
