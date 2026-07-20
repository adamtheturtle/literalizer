const std = @import("std");
fn make_widget(count: anytype) void { _ = count; }
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const my_data = make_widget((std.json.parseFromSlice(std.json.Value, allocator, "42", .{}) catch unreachable).value);
    _ = my_data;
}
