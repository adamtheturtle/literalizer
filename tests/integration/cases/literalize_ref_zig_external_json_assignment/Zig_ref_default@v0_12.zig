const std = @import("std");
fn consume_widget(_arg: anytype) void { _ = _arg; }
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const shared = (std.json.parseFromSlice(std.json.Value, allocator, "[1, 2]", .{}) catch unreachable).value;
    var my_data: std.json.Value = (std.json.parseFromSlice(std.json.Value, allocator, "[0]", .{}) catch unreachable).value;
    consume_widget(my_data);
    my_data = shared;
    consume_widget(my_data);
    _ = &my_data;
}
