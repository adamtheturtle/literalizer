const std = @import("std");
pub fn main() void {
    var @"literalizer JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"literalizer JSON arena".deinit();
    const allocator = @"literalizer JSON arena".allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "{\"date\": \"2024-01-15\", \"datetime\": \"2024-01-15T12:30:00+00:00\"}", .{}) catch unreachable).value;
    _ = my_data;
}
