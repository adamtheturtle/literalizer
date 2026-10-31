const Record0 = struct { a: i64 };
fn consume(value: anytype) void { _ = value; }
pub fn main() void {
    const item = Record0{
        .a = 1,
    };
    consume(item);
}
