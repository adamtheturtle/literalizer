const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "[\"line1\\r\\nline2\", \"line1\\rline2\", \"\\u0001\"]", .{}) catch unreachable).value;
    _ = my_data;
}
