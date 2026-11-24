const Record0 = struct { a: struct { i64, []const i64 } };
pub fn main() void {
    const my_data = Record0{
        .a = .{
            1,
            &.{},
        },
    };
    _ = my_data;
}
