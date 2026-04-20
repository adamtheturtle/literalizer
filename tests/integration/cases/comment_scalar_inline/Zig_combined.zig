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
    // note
    var my_data: ZVal = .{ .int = 42 };
    // note
    my_data = .{ .int = 42 };
    my_data = .nil;
}
