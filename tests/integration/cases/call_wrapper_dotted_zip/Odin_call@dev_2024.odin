#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }
_helpers_emit_ :: proc(args: ..any) -> any { return nil }
HelpersType_ :: struct { emit: proc(..any) -> any }

main :: proc() {
helpers: HelpersType_ = HelpersType_{ emit = _helpers_emit_ }
helpers.emit(process(1), 42);
}
