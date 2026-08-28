const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    // About a.
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "{\"a\": 1, \"b\": 2}", .{}) catch unreachable).value;
    _ = my_data;
}
