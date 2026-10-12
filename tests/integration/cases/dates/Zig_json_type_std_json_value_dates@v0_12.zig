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
        .{ .key = "date", .value = (std.json.parseFromSlice(std.json.Value, allocator, "\"2024-01-15\"", .{}) catch unreachable).value },
        .{ .key = "datetime", .value = (std.json.parseFromSlice(std.json.Value, allocator, "\"2024-01-15T12:30:00+00:00\"", .{}) catch unreachable).value },
    });
    _ = my_data;
}
