const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const my_data = std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{
        (std.json.parseFromSlice(std.json.Value, allocator, "true", .{}) catch unreachable).value,
        (std.json.parseFromSlice(std.json.Value, allocator, "false", .{}) catch unreachable).value,
        (std.json.parseFromSlice(std.json.Value, allocator, "true", .{}) catch unreachable).value,
    }) catch unreachable) };
    _ = my_data;
}
