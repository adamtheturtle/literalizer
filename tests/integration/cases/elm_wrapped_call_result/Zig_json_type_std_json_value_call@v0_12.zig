const std = @import("std");
fn make_widget(value: anytype) i64 { _ = value; return 0; }
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = make_widget((std.json.parseFromSlice(std.json.Value, allocator, "1", .{}) catch unreachable).value);
    _ = my_data;
}
