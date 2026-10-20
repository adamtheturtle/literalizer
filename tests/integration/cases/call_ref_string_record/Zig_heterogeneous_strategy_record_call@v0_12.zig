const Record0 = struct { value: []const u8 };
fn consume(value: anytype) void { _ = value; }
pub fn main() void {
    const item = Record0{
        .value = "owned",
    };
    consume(item);
}
