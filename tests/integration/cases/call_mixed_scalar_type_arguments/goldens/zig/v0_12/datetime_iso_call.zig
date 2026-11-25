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
const @"float std" = @import("std");
fn capture(nan_value: ZVal, positive_infinity: ZVal, negative_infinity: ZVal, finite_value: ZVal, date_value: ZVal, datetime_value: ZVal, text_value: ZVal) void { _ = nan_value; _ = positive_infinity; _ = negative_infinity; _ = finite_value; _ = date_value; _ = datetime_value; _ = text_value; }
pub fn main() void {
    capture(.{ .float = @"float std".math.nan(f64) }, .{ .float = @"float std".math.inf(f64) }, .{ .float = -@"float std".math.inf(f64) }, .{ .float = 1.25 }, .{ .int = 1705276800 }, .{ .str = "2024-01-15T12:34:56" }, .{ .str = "[ordinary text]" });
}
