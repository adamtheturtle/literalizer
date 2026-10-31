const Record0 = struct { a: i64 };
fn consume(stamp: anytype, value: anytype) void { _ = stamp; _ = value; }
pub fn main() void {
    const item = Record0{
        .a = 1,
    };
    const stamp = 981158400;
    consume(stamp, item);
}
