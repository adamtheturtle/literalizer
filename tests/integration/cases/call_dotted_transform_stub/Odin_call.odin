#+feature dynamic-literals
package main
process :: proc(args: ..any) -> any { return nil }
_log_emit_ :: proc(args: ..any) -> any { return nil }
LogType_ :: struct { emit: proc(..any) -> any }

main :: proc() {
log: LogType_ = LogType_{ emit = _log_emit_ }
log.emit(process("hello"));
log.emit(process(42));
log.emit(process(true));
}
