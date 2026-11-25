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
        .{ .key = "host", .val = .{ .str = "it's here" } },  // a comment
        .{ .key = "port", .val = .{ .int = 80 } },  // another
    }};
    my_data = .{ .map = &.{
        .{ .key = "host", .val = .{ .str = "it's here" } },  // a comment
        .{ .key = "port", .val = .{ .int = 80 } },  // another
    }};
    my_data = .nil;
}
