const std = @import("std");
fn consume(value: anytype) void { _ = value; }
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const shared = std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{
        (std.json.parseFromSlice(std.json.Value, allocator, "1", .{}) catch unreachable).value,
        (std.json.parseFromSlice(std.json.Value, allocator, "2", .{}) catch unreachable).value,
    }) catch unreachable) };
    consume((struct {
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
    }).@"literalizer JSON build"(allocator, &.{.{ .key = "field", .value = shared }, .{ .key = "nested", .value = std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{shared, std.json.Value{ .object = std.json.ObjectMap.init(allocator) }}) catch unreachable) } }}));
}
