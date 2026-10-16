const std = @import("std");
fn make_widget(value: anytype) i64 { _ = value; return 0; }
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const items = (std.json.parseFromSlice(std.json.Value, allocator, "[]", .{}) catch unreachable).value;
    make_widget(items);
}
