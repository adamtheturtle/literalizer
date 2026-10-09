const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    var shared: std.json.Value = (std.json.parseFromSlice(std.json.Value, allocator, "[1, 2]", .{}) catch unreachable).value;
    var my_data: std.json.Value = (std.json.parseFromSlice(std.json.Value, allocator, "{\"$ref\": \"shared\"}", .{}) catch unreachable).value;
    _ = &shared;
    _ = &my_data;
}
