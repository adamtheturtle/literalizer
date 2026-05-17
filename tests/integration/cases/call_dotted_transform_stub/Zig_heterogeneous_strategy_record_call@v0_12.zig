fn process(value: anytype) void { _ = value; }
const TracerType_ = struct { fn emit(self: TracerType_, _arg: anytype) void { _ = self; _ = _arg; } };
const tracer: TracerType_ = .{};
pub fn main() void {
    tracer.emit(process("hello"));
    tracer.emit(process(42));
    tracer.emit(process(true));
}
