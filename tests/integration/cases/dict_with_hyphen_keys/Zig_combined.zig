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
    var my_data: ZVal = .{ .map = &.{
        .{ .key = "my-key", .val = .{ .str = "value1" } },
        .{ .key = "another-key", .val = .{ .str = "value2" } },
        .{ .key = "normal_key", .val = .{ .str = "value3" } },
    }};
    my_data = .{ .map = &.{
        .{ .key = "my-key", .val = .{ .str = "value1" } },
        .{ .key = "another-key", .val = .{ .str = "value2" } },
        .{ .key = "normal_key", .val = .{ .str = "value3" } },
    }};
    my_data = .nil;
}
