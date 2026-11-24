fn f(a: anytype) void { _ = a; }
pub fn main() void {
    f(.{1, "x"});
}
