const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "[\"1901-12-13T20:45:51Z\", \"1901-12-13T20:45:52Z\", \"2038-01-19T03:14:07Z\", \"2038-01-19T03:14:08Z\"]", .{}) catch unreachable).value;
    _ = my_data;
}
