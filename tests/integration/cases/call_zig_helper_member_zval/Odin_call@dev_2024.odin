#+feature dynamic-literals
package main
_obj_ZVal_ :: proc(args: ..any) -> any { return nil }
ObjType_ :: struct { ZVal: proc(..any) -> any }

main :: proc() {
obj: ObjType_ = ObjType_{ ZVal = _obj_ZVal_ }
obj.ZVal(1);
}
