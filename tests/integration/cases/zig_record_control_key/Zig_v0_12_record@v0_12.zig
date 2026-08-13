const Record0 = struct { @"a\tb\nc": i64, id: []const u8 };
pub fn main() void {
    const my_data = &.{
        Record0{ .@"a\tb\nc" = 1, .id = "x" },
    };
    _ = my_data;
}
