const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "{\"quote\\\"backslash\\\\\": 1, \"line\\nbreak\": 2, \"$(literal)${text}\": 3, \"RStr prefix\": 4}", .{}) catch unreachable).value;
    _ = my_data;
}
