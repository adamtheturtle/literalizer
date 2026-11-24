const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{
        (std.json.parseFromSlice(std.json.Value, allocator, "\"48656c6c6f\"", .{}) catch unreachable).value,
        std.json.Value{ .array = std.json.Array.init(allocator) },
    }) catch unreachable) };
    _ = my_data;
}
