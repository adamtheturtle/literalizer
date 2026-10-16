const std = @import("std");
const ThingType_ = struct { fn go(self: ThingType_, before: anytype, populated: anytype, after: anytype) i64 { _ = self; _ = before; _ = populated; _ = after; return 0; } };
const thing: ThingType_ = .{};
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    thing.go(std.json.Value{ .array = std.json.Array.init(allocator) }, std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{(std.json.parseFromSlice(std.json.Value, allocator, "1", .{}) catch unreachable).value}) catch unreachable) }, std.json.Value{ .array = std.json.Array.init(allocator) });
    thing.go(std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{(std.json.parseFromSlice(std.json.Value, allocator, "\"text\"", .{}) catch unreachable).value}) catch unreachable) }, std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{(std.json.parseFromSlice(std.json.Value, allocator, "2", .{}) catch unreachable).value}) catch unreachable) }, std.json.Value{ .array = std.json.Array.init(allocator) });
    thing.go(std.json.Value{ .array = std.json.Array.init(allocator) }, std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{(std.json.parseFromSlice(std.json.Value, allocator, "\"text\"", .{}) catch unreachable).value}) catch unreachable) }, std.json.Value{ .array = std.json.Array.init(allocator) });
    thing.go(std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{(std.json.parseFromSlice(std.json.Value, allocator, "\"text\"", .{}) catch unreachable).value}) catch unreachable) }, std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{(std.json.parseFromSlice(std.json.Value, allocator, "2", .{}) catch unreachable).value}) catch unreachable) }, std.json.Value{ .array = std.json.Array.fromOwnedSlice(allocator, allocator.dupe(std.json.Value, &.{(std.json.parseFromSlice(std.json.Value, allocator, "3", .{}) catch unreachable).value}) catch unreachable) });
}
