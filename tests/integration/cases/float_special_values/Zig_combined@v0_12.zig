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
const @"literalizer float std" = @import("std");
pub fn main() void {
    var my_data: ZVal = .{ .arr = &.{
        .{ .float = @"literalizer float std".math.inf(f64) },
        .{ .float = -@"literalizer float std".math.inf(f64) },
        .{ .float = @"literalizer float std".math.nan(f64) },
    }};
    my_data = .{ .arr = &.{
        .{ .float = @"literalizer float std".math.inf(f64) },
        .{ .float = -@"literalizer float std".math.inf(f64) },
        .{ .float = @"literalizer float std".math.nan(f64) },
    }};
    my_data = .nil;
}
