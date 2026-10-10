const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const my_data = std.json.Value{ .object = std.json.ObjectMap.init(allocator) };
    _ = my_data;
}
