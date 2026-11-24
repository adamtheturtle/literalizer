const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    var shared: std.json.Value = (std.json.parseFromSlice(std.json.Value, allocator, "\"value\"", .{}) catch unreachable).value;
    var my_data: std.json.Value = shared;
    _ = &shared;
    _ = &my_data;
}
