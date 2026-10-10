const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    var my_data: std.json.Value = (std.json.parseFromSlice(std.json.Value, allocator, "{\"name\": \"Alice\", \"scores\": [10, 20, 30]}", .{}) catch unreachable).value;
    _ = &my_data;
}
