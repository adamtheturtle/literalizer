#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}
make_widget :: proc(args: ..any) -> any { return nil }

main :: proc() {
make_widget(_json_parse(`[]`), _json_parse(`[1]`), _json_parse(`[]`));
make_widget(_json_parse(`["text"]`), _json_parse(`[2]`), _json_parse(`[]`));
make_widget(_json_parse(`[]`), _json_parse(`["text"]`), _json_parse(`[]`));
make_widget(_json_parse(`["text"]`), _json_parse(`[2]`), _json_parse(`[3]`));
}
