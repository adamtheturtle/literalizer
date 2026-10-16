const std = @import("std");
fn make_widget(value: anytype) i64 { _ = value; return 0; }
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = make_widget(std.json.Value{ .array = std.json.Array.init(allocator) });
    _ = my_data;
}
