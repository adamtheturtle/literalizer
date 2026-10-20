const std = @import("std");
fn consume(value: anytype) void { _ = value; }
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const item = (std.json.parseFromSlice(std.json.Value, allocator, "\"s\"", .{}) catch unreachable).value;
    consume(item);
}
