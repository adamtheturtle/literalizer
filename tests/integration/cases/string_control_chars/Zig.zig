const ZVal = union(enum) {
    nil,
    bool: bool,
    int: i64,
    float: f64,
    str: []const u8,
    arr: []const ZVal,
    map: []const ZKV,
    set: []const ZVal,
};
const ZKV = struct { key: []const u8, val: ZVal };
pub fn main() void {
    const v: ZVal = .{ .arr = &.{
        .{ .str = "line1\nline2" },
        .{ .str = "line1line2" },
        .{ .str = "" },
    }};
    _ = v;
}
