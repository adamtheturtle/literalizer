pub fn main() void {
    const my_data = &.{
        .{ .key = "name", .val = "Alice" },
        .{ .key = "age", .val = 30 },
        .{ .key = "active", .val = true },
    };
    _ = my_data;
}
