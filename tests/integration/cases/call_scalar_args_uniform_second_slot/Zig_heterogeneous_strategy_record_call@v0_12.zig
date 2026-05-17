fn process(value: anytype, label: anytype) void { _ = value; _ = label; }
pub fn main() void {
    process("hello", "a");
    process(42, "b");
    process(true, "c");
}
