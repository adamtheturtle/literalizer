fn process(value: anytype) void { _ = value; }
pub fn main() void {
    process(.{"hello", 42, true});
}
