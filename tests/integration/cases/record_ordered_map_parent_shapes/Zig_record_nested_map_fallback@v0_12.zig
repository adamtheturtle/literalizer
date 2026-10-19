const Record2 = struct { x: i64 };
const Record1 = struct { values: []const struct { key: []const u8, val: Record2 }, flag: bool };
const Record4 = struct { y: i64 };
const Record3 = struct { values: []const struct { key: []const u8, val: Record4 }, flag: bool };
const Record0 = struct { first: Record1, second: Record3 };
pub fn main() void {
    const my_data = Record0{
        .first = Record1{
            .values = &.{
                .{ .key = "item", .val = Record2{
                    .x = 1,
                } },
            },
            .flag = true,
        },
        .second = Record3{
            .values = &.{
                .{ .key = "item", .val = Record4{
                    .y = 2,
                } },
            },
            .flag = false,
        },
    };
    _ = my_data;
}
