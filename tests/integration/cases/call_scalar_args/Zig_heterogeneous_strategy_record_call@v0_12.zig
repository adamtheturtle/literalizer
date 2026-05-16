fn process(value: anytype) void { _ = value; }
pub fn main() void {
    process("hello");
    process(42);
    process(true);
}
