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
    consume(std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{shared, (std.json.parseFromSlice(std.json.Value, allocator, "42", .{}) catch unreachable).value}) catch unreachable) });
}
