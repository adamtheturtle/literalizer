const std = @import("std");
fn process(value: anytype) void { _ = value; }
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    process((std.json.parseFromSlice(std.json.Value, allocator, "\"hello\"", .{}) catch unreachable).value);
    process((std.json.parseFromSlice(std.json.Value, allocator, "42", .{}) catch unreachable).value);
    process((std.json.parseFromSlice(std.json.Value, allocator, "true", .{}) catch unreachable).value);
}
