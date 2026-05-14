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
        // Configuration
        .{ .key = "name", .val = .{ .str = "app" } },
        // Port setting
        .{ .key = "port", .val = .{ .int = 3000 } },
    }};
    my_data = .{ .map = &.{
        // Configuration
        .{ .key = "name", .val = .{ .str = "app" } },
        // Port setting
        .{ .key = "port", .val = .{ .int = 3000 } },
    }};
    my_data = .nil;
}
