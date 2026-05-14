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
        .{ .key = "key\nwith\nnewlines", .val = .{ .str = "value1" } },
        .{ .key = "key\twith\ttabs", .val = .{ .str = "value2" } },
        .{ .key = "", .val = .{ .str = "value3" } },
    }};
    my_data = .{ .map = &.{
        .{ .key = "key\nwith\nnewlines", .val = .{ .str = "value1" } },
        .{ .key = "key\twith\ttabs", .val = .{ .str = "value2" } },
        .{ .key = "", .val = .{ .str = "value3" } },
    }};
    my_data = .nil;
}
