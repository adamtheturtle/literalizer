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
    {
        const my_data: ZVal = .{ .year = 2024, .month = 1, .day = 15 };
        _ = my_data;
    }
    var my_data: ZVal = undefined;
    my_data = .{ .year = 2024, .month = 1, .day = 15 };
    const _my_data_read = my_data;
    _ = _my_data_read;
}
