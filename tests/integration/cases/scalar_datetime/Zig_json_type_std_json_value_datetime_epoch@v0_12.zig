const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "\"2024-01-15T12:30:00+00:00\"", .{}) catch unreachable).value;
    _ = my_data;
}
