const std = @import("std");
fn consume(value: anytype) void { _ = value; }
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const shared = (std.json.parseFromSlice(std.json.Value, allocator, "[1, 2]", .{}) catch unreachable).value;
    consume((struct {
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
    }).@"JSON build"(allocator, &.{.{ .key = "field", .value = shared }, .{ .key = "nested", .value = std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{shared, std.json.Value{ .object = std.json.ObjectMap.init(allocator) }}) catch unreachable) } }}));
}
