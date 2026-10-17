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
        .{ .key = "name", .value = (std.json.parseFromSlice(std.json.Value, allocator, "\"Alice\"", .{}) catch unreachable).value },
        .{ .key = "scores", .value = std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{
            (std.json.parseFromSlice(std.json.Value, allocator, "10", .{}) catch unreachable).value,
            (std.json.parseFromSlice(std.json.Value, allocator, "20", .{}) catch unreachable).value,
            (std.json.parseFromSlice(std.json.Value, allocator, "30", .{}) catch unreachable).value,
        }) catch unreachable) } },
    });
    _ = my_data;
}
