const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "{\"name\": \"Alice\", \"age\": 30, \"active\": true}", .{}) catch unreachable).value;
    _ = my_data;
}
