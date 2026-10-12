const @"record value" = union(enum) {
    nil,
    bool: bool,
    int: i64,
    uint: u64,
    float: f64,
    str: []const u8,
    arr: []const @"record value",
    map: []const @"record entry",
    set: []const @"record value",
};
const @"record entry" = struct { key: []const u8, val: @"record value" };
const Record0 = struct { input: @"record value" };
pub fn main() void {
    const my_data = &.{
        Record0{
            .input = .{ .map = &.{
                .{ .key = "a", .val = .{ .int = 1 } },
            }},
        },
        Record0{
            .input = .{ .map = &.{
                .{ .key = "b", .val = .nil },
            }},
        },
    };
    _ = my_data;
}
