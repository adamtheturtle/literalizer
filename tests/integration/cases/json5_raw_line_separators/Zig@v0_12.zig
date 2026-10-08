const ZVal = union(enum) {
    nil,
    bool: bool,
    int: i64,
    uint: u64,
    float: f64,
    str: []const u8,
    arr: []const ZVal,
    map: []const ZKV,
    set: []const ZVal,
};
const ZKV = struct { key: []const u8, val: ZVal };
pub fn main() void {
    const my_data: ZVal = .{ .map = &.{
        .{ .key = "double", .val = .{ .str = "a     b" } },
        .{ .key = "single", .val = .{ .str = "c     d" } },
        .{ .key = "both", .val = .{ .str = "e     f     g" } },
        .{ .key = "continued", .val = .{ .str = "hi" } },
        .{ .key = "escaped backslash", .val = .{ .str = "j\\     k" } },
    }};
    _ = my_data;
}
