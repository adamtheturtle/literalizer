fn process(value: anytype, extra: anytype) void { _ = value; _ = extra; }
pub fn main() void {
    process(1, "hello");
    process("two", false);
    process(3.5, null);
}
