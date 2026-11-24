const Record0 = struct { a: i64 };
fn consume(stamp: anytype, value: anytype) void { _ = stamp; _ = value; }
pub fn main() void {
    const stamp = 981158400;
    const item = Record0{
        .a = 1,
    };
    consume(stamp, item);
}
