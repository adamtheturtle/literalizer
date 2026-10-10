const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const my_data = std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{
        std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{(std.json.parseFromSlice(std.json.Value, allocator, "1", .{}) catch unreachable).value, (std.json.parseFromSlice(std.json.Value, allocator, "\"a\"", .{}) catch unreachable).value}) catch unreachable) },
        std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{(std.json.parseFromSlice(std.json.Value, allocator, "2", .{}) catch unreachable).value, (std.json.parseFromSlice(std.json.Value, allocator, "\"b\"", .{}) catch unreachable).value}) catch unreachable) },
    }) catch unreachable) };
    _ = my_data;
}
