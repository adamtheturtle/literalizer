#+feature dynamic-literals
package main
import "core:encoding/json"
_json_parse :: proc(s: string) -> json.Value {
	v, _ := json.parse_string(s, parse_integers=true)
	return v
}
_obj_ZVal_ :: proc(args: ..any) -> any { return nil }
ObjType_ :: struct { ZVal: proc(..any) -> any }

main :: proc() {
obj: ObjType_ = ObjType_{ ZVal = _obj_ZVal_ }
obj.ZVal(_json_parse(`1`));
}
