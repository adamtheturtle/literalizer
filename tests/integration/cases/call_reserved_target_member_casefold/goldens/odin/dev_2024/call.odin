#+feature dynamic-literals
package main
_obj_BEGIN_ :: proc(args: ..any) -> any { return nil }
ObjType_ :: struct { BEGIN: proc(..any) -> any }

main :: proc() {
obj: ObjType_ = ObjType_{ BEGIN = _obj_BEGIN_ }
obj.BEGIN(42);
}
