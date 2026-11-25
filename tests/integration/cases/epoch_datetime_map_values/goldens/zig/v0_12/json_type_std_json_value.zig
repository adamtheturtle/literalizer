const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = (struct {
        fn @"JSON build"(
            @"JSON allocator": std.mem.Allocator,
            @"JSON entries": []const struct {
                key: []const u8,
                value: std.json.Value,
            },
        ) std.json.Value {
            var @"JSON object" =
                std.json.ObjectMap.init(@"JSON allocator");
            for (@"JSON entries") |@"JSON entry"| {
                @"JSON object".put(
                    @"JSON entry".key,
                    @"JSON entry".value,
                ) catch unreachable;
            }
            return .{ .object = @"JSON object" };
        }
    }).@"JSON build"(allocator, &.{
        .{ .key = "within_i32", .value = (std.json.parseFromSlice(std.json.Value, allocator, "\"2024-01-15T12:00:00Z\"", .{}) catch unreachable).value },
        .{ .key = "beyond_i32", .value = (std.json.parseFromSlice(std.json.Value, allocator, "\"2099-06-15T08:30:00Z\"", .{}) catch unreachable).value },
    });
    _ = my_data;
}
