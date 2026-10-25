const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "\"2024-01-15T18:00:00+05:00\"", .{}) catch unreachable).value;
    _ = my_data;
}
