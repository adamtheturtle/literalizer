#+feature dynamic-literals
package main
_obj_ZKV_ :: proc(args: ..any) -> any { return nil }
ObjType_ :: struct { ZKV: proc(..any) -> any }

main :: proc() {
obj: ObjType_ = ObjType_{ ZKV = _obj_ZKV_ }
obj.ZKV(1);
}
