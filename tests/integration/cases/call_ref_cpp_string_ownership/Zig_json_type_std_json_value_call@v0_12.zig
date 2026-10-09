const std = @import("std");
fn consume(value: anytype) void { _ = value; }
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const item = (std.json.parseFromSlice(std.json.Value, allocator, "\"s\"", .{}) catch unreachable).value;
    consume(item);
}
