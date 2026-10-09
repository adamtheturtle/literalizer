const std = @import("std");
fn consume(value: anytype) void { _ = value; }
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const my_null = (std.json.parseFromSlice(std.json.Value, allocator, "null", .{}) catch unreachable).value;
    const regular_null = (std.json.parseFromSlice(std.json.Value, allocator, "null", .{}) catch unreachable).value;
    consume(my_null);
    consume(regular_null);
}
