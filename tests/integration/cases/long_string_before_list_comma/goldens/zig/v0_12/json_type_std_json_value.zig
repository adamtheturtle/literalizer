const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "[\"This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.\", 1]", .{}) catch unreachable).value;
    _ = my_data;
}
