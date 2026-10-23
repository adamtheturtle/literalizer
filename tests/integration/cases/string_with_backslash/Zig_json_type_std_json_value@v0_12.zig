const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{
        (std.json.parseFromSlice(std.json.Value, allocator, "\"C:\\\\path\\\\to\\\\file\"", .{}) catch unreachable).value,
        (std.json.parseFromSlice(std.json.Value, allocator, "\"back\\\\\\\\slash\"", .{}) catch unreachable).value,
        (std.json.parseFromSlice(std.json.Value, allocator, "\"hello \\\\\\\"world\\\\\\\"\"", .{}) catch unreachable).value,
        (std.json.parseFromSlice(std.json.Value, allocator, "\"path\\\\to \\\"# file\"", .{}) catch unreachable).value,
        (std.json.parseFromSlice(std.json.Value, allocator, "\"trailing\\\\\"", .{}) catch unreachable).value,
        (std.json.parseFromSlice(std.json.Value, allocator, "\"both \\\"quotes''' here\"", .{}) catch unreachable).value,
        (std.json.parseFromSlice(std.json.Value, allocator, "\"line1\\\\nline2\\nwith newline\"", .{}) catch unreachable).value,
    }) catch unreachable) };
    _ = my_data;
}
