const std = @import("std");
pub fn main() void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();
    const my_data = (struct {
        fn @"literalizer JSON build"(
            @"literalizer JSON allocator": std.mem.Allocator,
            @"literalizer JSON entries": []const struct {
                key: []const u8,
                value: std.json.Value,
            },
        ) std.json.Value {
            var @"literalizer JSON object" =
                std.json.ObjectMap.init(@"literalizer JSON allocator");
            for (@"literalizer JSON entries") |@"literalizer JSON entry"| {
                @"literalizer JSON object".put(
                    @"literalizer JSON entry".key,
                    @"literalizer JSON entry".value,
                ) catch unreachable;
            }
            return .{ .object = @"literalizer JSON object" };
        }
    }).@"literalizer JSON build"(allocator, &.{
        .{ .key = ")json", .value = (std.json.parseFromSlice(std.json.Value, allocator, "\"x\"", .{}) catch unreachable).value },
    });
    _ = my_data;
}
