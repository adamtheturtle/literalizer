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
    const custom_data: ZVal = .{ .str = "head\nfinal my_data = 123;\nfinal fakeRoot = 1;\nfinal fixtureRoot = 1;\ntail" };
    _ = custom_data;
}
