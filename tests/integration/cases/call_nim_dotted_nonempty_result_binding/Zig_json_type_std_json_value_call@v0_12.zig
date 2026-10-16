const std = @import("std");
const ThingType_ = struct { fn go(self: ThingType_, value: anytype) i64 { _ = self; _ = value; return 0; } };
const thing: ThingType_ = .{};
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = thing.go(std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{(std.json.parseFromSlice(std.json.Value, allocator, "1", .{}) catch unreachable).value}) catch unreachable) });
    _ = my_data;
}
