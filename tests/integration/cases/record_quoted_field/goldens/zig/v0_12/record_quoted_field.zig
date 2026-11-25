const Record0 = struct { @"a-b": i64 };
pub fn main() void {
    const my_data = &.{
        Record0{ .@"a-b" = 1 },
    };
    _ = my_data;
}
