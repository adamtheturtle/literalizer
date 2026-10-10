const std = @import("std");
pub fn main() void {
    var @"literalizer JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"literalizer JSON arena".deinit();
    const allocator = @"literalizer JSON arena".allocator();
    const arena = (std.json.parseFromSlice(std.json.Value, allocator, "{\"a\": 1}", .{}) catch unreachable).value;
    _ = arena;
}
