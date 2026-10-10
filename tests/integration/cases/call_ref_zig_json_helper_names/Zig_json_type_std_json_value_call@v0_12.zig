const std = @import("std");
fn process(value: anytype) void { _ = value; }
pub fn main() void {
    var @"literalizer JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"literalizer JSON arena".deinit();
    const allocator = @"literalizer JSON arena".allocator();
    const arena = (std.json.parseFromSlice(std.json.Value, allocator, "{\"a\": 1}", .{}) catch unreachable).value;
    const ZVal = (std.json.parseFromSlice(std.json.Value, allocator, "{\"a\": 1}", .{}) catch unreachable).value;
    const ZKV = (std.json.parseFromSlice(std.json.Value, allocator, "{\"a\": 1}", .{}) catch unreachable).value;
    process(arena);
    process(ZVal);
    process(ZKV);
}
