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
    // scalar inline
    // inline continuation
    // scalar trailing
    var my_data: ZVal = .{ .int = // scalar heading
    // second heading line
    42 };
    // scalar inline
    // inline continuation
    // scalar trailing
    my_data = .{ .int = // scalar heading
    // second heading line
    42 };
    my_data = .nil;
}
