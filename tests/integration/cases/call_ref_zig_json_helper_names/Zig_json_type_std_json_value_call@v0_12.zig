const std = @import("std");
fn process(value: anytype) void { _ = value; }
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const arena = (std.json.parseFromSlice(std.json.Value, allocator, "{\"a\": 1}", .{}) catch unreachable).value;
    const ZVal = (std.json.parseFromSlice(std.json.Value, allocator, "{\"a\": 1}", .{}) catch unreachable).value;
    const ZKV = (std.json.parseFromSlice(std.json.Value, allocator, "{\"a\": 1}", .{}) catch unreachable).value;
    process(arena);
    process(ZVal);
    process(ZKV);
}
