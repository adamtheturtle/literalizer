const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const shared = (struct {
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
        .{ .key = "field", .value = std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{(std.json.parseFromSlice(std.json.Value, allocator, "1", .{}) catch unreachable).value, (std.json.parseFromSlice(std.json.Value, allocator, "2", .{}) catch unreachable).value}) catch unreachable) } },
    });
    const my_data: std.json.Value = shared;
    _ = my_data;
}
