const std = @import("std");
pub fn main() void {
    var @"literalizer JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"literalizer JSON arena".deinit();
    const allocator = @"literalizer JSON arena".allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "{\"name\": \"Alice\", \"score\": null, \"age\": 30}", .{}) catch unreachable).value;
    _ = my_data;
}
