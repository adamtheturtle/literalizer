const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const ZVal = (std.json.parseFromSlice(std.json.Value, allocator, "{\"a\": 1}", .{}) catch unreachable).value;
    _ = ZVal;
}
