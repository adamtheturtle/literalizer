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
                const shared: ZVal = .{ .arr = &.{
                    .{ .int = 1 },
                    .{ .int = 2 },
                }};
                const other: ZVal = .{ .int = 3 };
                const payload: ZVal = .{ .str = "\n    shared : Val\nshared = RInt 99" };
                const my_data: ZVal = .{ .map = &.{
                    .{ .key = "a", .val = shared },
                    .{ .key = "b", .val = other },
                    .{ .key = "payload", .val = payload },
                }};
    _ = my_data;
}
