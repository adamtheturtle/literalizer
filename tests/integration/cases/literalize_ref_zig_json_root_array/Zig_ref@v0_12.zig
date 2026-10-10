const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const shared = (std.json.parseFromSlice(std.json.Value, allocator, "[1, 2]", .{}) catch unreachable).value;
    const my_data: std.json.Value = shared;
    _ = my_data;
}
