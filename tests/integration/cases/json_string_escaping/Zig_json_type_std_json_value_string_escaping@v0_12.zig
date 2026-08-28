const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "{\"$key\": \"a\\\"b\\tcé #{world} $ident\", \"trailing multi-byte\": \"café\"}", .{}) catch unreachable).value;
    _ = my_data;
}
