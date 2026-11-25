const std = @import("std");
fn make_widget(value: anytype) void { _ = value; }
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const value = (std.json.parseFromSlice(std.json.Value, allocator, "1", .{}) catch unreachable).value;
    make_widget(value);
}
