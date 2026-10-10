const std = @import("std");
pub fn main() void {
    var @"literalizer JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"literalizer JSON arena".deinit();
    const allocator = @"literalizer JSON arena".allocator();
    const shared = (std.json.parseFromSlice(std.json.Value, allocator, "\"value\"", .{}) catch unreachable).value;
    const my_data: std.json.Value = shared;
    _ = my_data;
}
