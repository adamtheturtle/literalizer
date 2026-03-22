const ZDate = struct { year: i32, month: u8, day: u8 };
const ZDatetime = struct { year: i32, month: u8, day: u8, hour: u8, minute: u8, second: u8 };
const ZVal = union(enum) {
    nil,
    bool: bool,
    int: i64,
    float: f64,
    str: []const u8,
    arr: []const ZVal,
    map: []const ZKV,
    set: []const ZVal,
    date: ZDate,
    datetime: ZDatetime,
};
const ZKV = struct { key: []const u8, val: ZVal };
pub fn main() void {
    const my_data: ZVal = .{ .map = &.{
        .{ .key = "name", .val = .{ .str = "Alice" } },
        .{ .key = "age", .val = .{ .int = 30 } },
        .{ .key = "active", .val = .{ .bool = true } },
    }};
    _ = my_data;
}
