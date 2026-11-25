const Record0 = struct { type: []const u8, match: []const u8, @"error": []const u8, @"switch": []const u8, class: []const u8, inout: []const u8, int: []const u8, new: []const u8, static: []const u8, fun: []const u8, object: []const u8, val: []const u8, when: []const u8, func: []const u8, let: []const u8, @"var": []const u8, template: []const u8, id: i64 };
pub fn main() void {
    const my_data = &.{
        Record0{ .type = "a", .match = "b", .@"error" = "c", .@"switch" = "d", .class = "e", .inout = "ee", .int = "f", .new = "g", .static = "h", .fun = "i", .object = "j", .val = "k", .when = "l", .func = "m", .let = "n", .@"var" = "o", .template = "p", .id = 1 },
    };
    _ = my_data;
}
