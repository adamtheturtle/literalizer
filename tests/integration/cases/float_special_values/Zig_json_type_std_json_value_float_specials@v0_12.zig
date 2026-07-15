const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "[Infinity, -Infinity, NaN]", .{}) catch unreachable).value;
    _ = my_data;
}
