const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const my_data = std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{
        (std.json.parseFromSlice(std.json.Value, allocator, "9223372036854775807", .{}) catch unreachable).value,
        (std.json.parseFromSlice(std.json.Value, allocator, "9223372036854775808", .{}) catch unreachable).value,
    }) catch unreachable) };
    _ = my_data;
}
