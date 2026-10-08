const Record1 = struct { k: []const bool };
const Record0 = struct { h: struct { i64, []const u8, struct { i64, []const u8 }, []const u8 } };
pub fn main() void {
    const my_data = Record0{
        .h = .{
            1,
            "a",
            .{
                2,
                "b",
            },
            Record1{
                .k = &.{
                    true,
                },
            },
        },
    };
    _ = my_data;
}
