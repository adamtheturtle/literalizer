const std = @import("std");
pub fn main() void {
    var @"literalizer JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"literalizer JSON arena".deinit();
    const allocator = @"literalizer JSON arena".allocator();
    const my_data = (struct {
        fn @"literalizer JSON build"(
            @"literalizer JSON allocator": std.mem.Allocator,
            @"literalizer JSON entries": []const struct {
                key: []const u8,
                value: std.json.Value,
            },
        ) std.json.Value {
            var @"literalizer JSON object" =
                std.json.ObjectMap.init(@"literalizer JSON allocator");
            for (@"literalizer JSON entries") |@"literalizer JSON entry"| {
                @"literalizer JSON object".put(
                    @"literalizer JSON entry".key,
                    @"literalizer JSON entry".value,
                ) catch unreachable;
            }
            return .{ .object = @"literalizer JSON object" };
        }
    }).@"literalizer JSON build"(allocator, &.{
        .{ .key = "date", .value = (std.json.parseFromSlice(std.json.Value, allocator, "\"2024-01-15\"", .{}) catch unreachable).value },
        .{ .key = "datetime", .value = (std.json.parseFromSlice(std.json.Value, allocator, "\"2024-01-15T12:30:00+00:00\"", .{}) catch unreachable).value },
    });
    _ = my_data;
}
