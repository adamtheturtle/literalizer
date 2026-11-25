const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "\"\\nroot first line\\n  indented\\n\\nroot last line\\n\"", .{}) catch unreachable).value;
    _ = my_data;
}
