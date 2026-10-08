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
const Record0 = struct { input: ZVal };
pub fn main() void {
    const my_data = &.{
        Record0{
            .input = .{ .map = &.{
                .{ .key = "a", .val = .{ .int = 1 } },
            }},
        },
        Record0{
            .input = .{ .map = &.{
                .{ .key = "b", .val = .{ .int = 2 } },
            }},
        },
    };
    _ = my_data;
}
