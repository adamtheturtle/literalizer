const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "{\"__proto__\": {\"x\": 1}, \"n\": {\"__proto__\": 3}, \"y\": 2}", .{}) catch unreachable).value;
    _ = my_data;
}
