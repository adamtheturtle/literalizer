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
        .{ .key = "half", .val = .{ .str = "1979-05-27T07:32:00.500000" } },
        .{ .key = "milli", .val = .{ .str = "1979-05-27T07:32:00.100000" } },
        .{ .key = "max_milli", .val = .{ .str = "1979-05-27T07:32:00.999000" } },
        .{ .key = "whole", .val = .{ .str = "1979-05-27T07:32:00" } },
    }};
    _ = my_data;
}
