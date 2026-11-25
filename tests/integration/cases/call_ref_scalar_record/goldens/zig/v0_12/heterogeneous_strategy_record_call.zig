const Record0 = struct { value: i64 };
fn consume(value: anytype) void { _ = value; }
pub fn main() void {
    const item = Record0{
        .value = 1,
    };
    consume(item);
}
