#+feature dynamic-literals
package main
_obj_class_ :: proc(args: ..any) -> any { return nil }
ObjType_ :: struct { class: proc(..any) -> any }

main :: proc() {
obj: ObjType_ = ObjType_{ class = _obj_class_ }
obj.class(42);
}
