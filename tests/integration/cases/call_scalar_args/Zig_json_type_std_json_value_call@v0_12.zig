const std = @import("std");
fn process(value: anytype) void { _ = value; }
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    process((std.json.parseFromSlice(std.json.Value, allocator, "\"hello\"", .{}) catch unreachable).value);
    process((std.json.parseFromSlice(std.json.Value, allocator, "42", .{}) catch unreachable).value);
    process((std.json.parseFromSlice(std.json.Value, allocator, "true", .{}) catch unreachable).value);
}
