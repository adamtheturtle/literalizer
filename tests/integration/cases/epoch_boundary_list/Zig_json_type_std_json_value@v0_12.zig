const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{
        (std.json.parseFromSlice(std.json.Value, allocator, "\"1901-12-13T20:45:51Z\"", .{}) catch unreachable).value,
        (std.json.parseFromSlice(std.json.Value, allocator, "\"1901-12-13T20:45:52Z\"", .{}) catch unreachable).value,
        (std.json.parseFromSlice(std.json.Value, allocator, "\"2038-01-19T03:14:07Z\"", .{}) catch unreachable).value,
        (std.json.parseFromSlice(std.json.Value, allocator, "\"2038-01-19T03:14:08Z\"", .{}) catch unreachable).value,
    }) catch unreachable) };
    _ = my_data;
}
