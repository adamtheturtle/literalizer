fn process(value: anytype) void { _ = value; }
pub fn main() void {
    process(null);
    process("hello");
}
