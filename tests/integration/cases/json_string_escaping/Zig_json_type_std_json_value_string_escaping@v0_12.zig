const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const my_data = (struct {
        fn @"JSON build"(
            @"JSON allocator": std.mem.Allocator,
            @"JSON entries": []const struct {
                key: []const u8,
                value: std.json.Value,
            },
        ) std.json.Value {
            var @"JSON object" =
                std.json.ObjectMap.init(@"JSON allocator");
            for (@"JSON entries") |@"JSON entry"| {
                @"JSON object".put(
                    @"JSON entry".key,
                    @"JSON entry".value,
                ) catch unreachable;
            }
            return .{ .object = @"JSON object" };
        }
    }).@"JSON build"(allocator, &.{
        .{ .key = "$key", .value = (std.json.parseFromSlice(std.json.Value, allocator, "\"a\\\"b\\tcé #{world} $ident\"", .{}) catch unreachable).value },
        .{ .key = "trailing multi-byte", .value = (std.json.parseFromSlice(std.json.Value, allocator, "\"café\"", .{}) catch unreachable).value },
    });
    _ = my_data;
}
