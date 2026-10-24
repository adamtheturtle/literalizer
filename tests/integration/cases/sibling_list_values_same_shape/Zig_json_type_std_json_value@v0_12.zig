const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "{\"test\": [5, [\"compile\", \"test\"]], \"package\": [7, [\"link\", \"test\"]]}", .{}) catch unreachable).value;
    _ = my_data;
}
