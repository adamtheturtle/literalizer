const Record0 = struct { name: []const u8, values: []const i64 };
fn consume(value: anytype) void { _ = value; }
pub fn main() void {
    const item = Record0{
        .name = "first",
        .values = &.{
            1,
            2,
        },
    };
    consume(item);
}
