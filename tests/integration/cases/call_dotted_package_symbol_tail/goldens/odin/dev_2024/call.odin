#+feature dynamic-literals
package main
_helper_list_ :: proc(args: ..any) -> any { return nil }
HelperType_ :: struct { list: proc(..any) -> any }

main :: proc() {
helper: HelperType_ = HelperType_{ list = _helper_list_ }
helper.list(1);
}
