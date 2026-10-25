const std = @import("std");
fn consume(value: anytype) void { _ = value; }
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const shared = (std.json.parseFromSlice(std.json.Value, allocator, "42", .{}) catch unreachable).value;
    consume(std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{shared, shared}) catch unreachable) });
}
