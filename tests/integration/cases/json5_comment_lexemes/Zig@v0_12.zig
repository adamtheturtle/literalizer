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
        // heading
        .{ .key = "a", .val = .{ .str = "single ' // data" } },
        .{ .key = "b", .val = .{ .str = "linecontinuation" } },
        .{ .key = "c", .val = .{ .str = "\\" } },  // actual comment
        .{ .key = "d", .val = .{ .str = "      " } },  // final comment
    }};
    _ = my_data;
}
