const Record0 = struct { type: []const u8, match: []const u8, @"error": []const u8, @"switch": []const u8, id: i64 };
pub fn main() void {
    const my_data = &.{
        Record0{ .type = "a", .match = "b", .@"error" = "c", .@"switch" = "d", .id = 1 },
    };
    _ = my_data;
}
