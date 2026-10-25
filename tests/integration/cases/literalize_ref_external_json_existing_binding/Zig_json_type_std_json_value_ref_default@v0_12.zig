const std = @import("std");
fn consume_widget(arg_value: anytype) void { _ = arg_value; }
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    var my_data: std.json.Value = (std.json.parseFromSlice(std.json.Value, allocator, "{\"a\": 0}", .{}) catch unreachable).value;
    consume_widget(my_data);
    my_data = (std.json.parseFromSlice(std.json.Value, allocator, "{\"a\": 1}", .{}) catch unreachable).value;
    consume_widget(my_data);
    _ = &my_data;
}
