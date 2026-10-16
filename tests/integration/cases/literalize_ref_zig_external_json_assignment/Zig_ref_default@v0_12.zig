const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const shared = (std.json.parseFromSlice(std.json.Value, allocator, "[1, 2]", .{}) catch unreachable).value;
    var my_data: std.json.Value = (std.json.parseFromSlice(std.json.Value, allocator, "[0]", .{}) catch unreachable).value;
    _ = &my_data;
    my_data = shared;
    _ = &my_data;
    _ = &my_data;
}
