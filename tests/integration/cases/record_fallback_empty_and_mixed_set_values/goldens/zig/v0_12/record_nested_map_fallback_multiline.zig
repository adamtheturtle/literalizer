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
const Record0 = struct { name: []const u8, payload: @"record value" };
pub fn main() void {
    const my_data = &.{
        Record0{
            .name = "one",
            .payload = .{ .map = &.{
                .{ .key = "scalar", .val = .{ .int = 1 } },
                .{ .key = "empty", .val = .{ .set = &.{}} },
                .{ .key = "mixed", .val = .{ .set = &.{
                    .{ .int = 2 },
                    .{ .str = "word" },
                }} },
            }},
        },
        Record0{
            .name = "two",
            .payload = .{ .map = &.{
                .{ .key = "other", .val = .{ .int = 2 } },
            }},
        },
    };
    _ = my_data;
}
