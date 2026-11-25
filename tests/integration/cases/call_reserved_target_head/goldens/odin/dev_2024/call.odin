#+feature dynamic-literals
package main
_class_member_ :: proc(args: ..any) -> any { return nil }
ClassType_ :: struct { member: proc(..any) -> any }

main :: proc() {
class: ClassType_ = ClassType_{ member = _class_member_ }
class.member(42);
}
