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
fn process(p0: ZVal, p1: ZVal, p2: ZVal, p3: ZVal, p4: ZVal, p5: ZVal, p6: ZVal, p7: ZVal, p8: ZVal, p9: ZVal, p10: ZVal, p11: ZVal, p12: ZVal, p13: ZVal, p14: ZVal, p15: ZVal, p16: ZVal, p17: ZVal, p18: ZVal, p19: ZVal, p20: ZVal, p21: ZVal, p22: ZVal, p23: ZVal, p24: ZVal, p25: ZVal, p26: ZVal) void { _ = p0; _ = p1; _ = p2; _ = p3; _ = p4; _ = p5; _ = p6; _ = p7; _ = p8; _ = p9; _ = p10; _ = p11; _ = p12; _ = p13; _ = p14; _ = p15; _ = p16; _ = p17; _ = p18; _ = p19; _ = p20; _ = p21; _ = p22; _ = p23; _ = p24; _ = p25; _ = p26; }
pub fn main() void {
    process(.{ .int = 0 }, .{ .int = 1 }, .{ .int = 2 }, .{ .int = 3 }, .{ .int = 4 }, .{ .int = 5 }, .{ .int = 6 }, .{ .int = 7 }, .{ .int = 8 }, .{ .int = 9 }, .{ .int = 10 }, .{ .int = 11 }, .{ .int = 12 }, .{ .int = 13 }, .{ .int = 14 }, .{ .int = 15 }, .{ .int = 16 }, .{ .int = 17 }, .{ .int = 18 }, .{ .int = 19 }, .{ .int = 20 }, .{ .int = 21 }, .{ .int = 22 }, .{ .int = 23 }, .{ .int = 24 }, .{ .int = 25 }, .{ .int = 26 });
}
