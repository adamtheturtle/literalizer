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
    print(throttler.check("user_1", 1000.0))
    print(throttler.check("user_2", 2000.5))
    _ = my_data;
}
