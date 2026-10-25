#+feature dynamic-literals
package main
_obj_ZVal_ :: proc(args: ..any) -> any { return nil }
ObjType_ :: struct { ZVal: proc(..any) -> any }

main :: proc() {
obj: ObjType_ = ObjType_{ ZVal = _obj_ZVal_ }
my_data := obj.ZVal(42) // note
_ = my_data
}
