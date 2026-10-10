const std = @import("std");
const ObjType_ = struct { fn std(self: ObjType_, value: anytype) void { _ = self; _ = value; } };
const obj: ObjType_ = .{};
pub fn main() void {
    var @"literalizer JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"literalizer JSON arena".deinit();
    const allocator = @"literalizer JSON arena".allocator();
    obj.std((std.json.parseFromSlice(std.json.Value, allocator, "1", .{}) catch unreachable).value);
}
