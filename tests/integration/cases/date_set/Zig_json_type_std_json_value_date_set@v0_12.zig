const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "[\"2024-01-15\", \"2024-06-01\"]", .{}) catch unreachable).value;
    _ = my_data;
}
