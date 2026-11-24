const std = @import("std");
fn consume_widget(arg_value: anytype) void { _ = arg_value; }
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const item = (std.json.parseFromSlice(std.json.Value, allocator, "null", .{}) catch unreachable).value;
    var my_data: std.json.Value = (std.json.parseFromSlice(std.json.Value, allocator, "null", .{}) catch unreachable).value;
    consume_widget(my_data);
    my_data = item;
    consume_widget(my_data);
    _ = &my_data;
}
