const std = @import("std");
fn consume_widget(arg_value: anytype) void { _ = arg_value; }
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const shared = (std.json.parseFromSlice(std.json.Value, allocator, "[1, 2]", .{}) catch unreachable).value;
    const my_data: std.json.Value = shared;
    consume_widget(my_data);
}
