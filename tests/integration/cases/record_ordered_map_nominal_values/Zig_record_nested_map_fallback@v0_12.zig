const Record1 = struct { x: i64 };
const Record0 = struct { values: []const struct { key: []const u8, val: Record1 }, flag: bool };
pub fn main() void {
    const my_data = Record0{
        .values = &.{
            .{ .key = "first", .val = Record1{
                .x = 1,
            } },
            .{ .key = "second", .val = Record1{
                .x = 2,
            } },
        },
        .flag = true,
    };
    _ = my_data;
}
