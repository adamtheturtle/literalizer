const std = @import("std");
fn process(data: anytype) void { _ = data; }
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const untyped_value = (std.json.parseFromSlice(std.json.Value, allocator, "[]", .{}) catch unreachable).value;
    process(std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{untyped_value, untyped_value}) catch unreachable) });
}
