const Record1 = struct { x: i64 };
const Record0 = struct { values: []const []const struct { key: []const u8, val: Record1 }, flag: bool };
pub fn main() void {
    const my_data = Record0{
        .values = &.{
            &.{
                .{ .key = "inner", .val = Record1{
                    .x = 1,
                } },
            },
            &.{
                .{ .key = "inner", .val = Record1{
                    .x = 2,
                } },
            },
        },
        .flag = true,
    };
    _ = my_data;
}
