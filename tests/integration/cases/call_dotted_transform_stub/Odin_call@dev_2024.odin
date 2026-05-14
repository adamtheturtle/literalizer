#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }
_tracer_emit_ :: proc(args: ..any) -> any { return nil }
TracerType_ :: struct { emit: proc(..any) -> any }

main :: proc() {
tracer: TracerType_ = TracerType_{ emit = _tracer_emit_ }
tracer.emit(process("hello"));
tracer.emit(process(42));
tracer.emit(process(true));
}
