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
    const my_data: ZVal = .{ .map = &.{
        .{ .key = "if", .val = .{ .int = 1 } },
        .{ .key = "then", .val = .{ .int = 2 } },
        .{ .key = "else", .val = .{ .int = 3 } },
        .{ .key = "let", .val = .{ .int = 4 } },
        .{ .key = "in", .val = .{ .int = 5 } },
        .{ .key = "using", .val = .{ .int = 6 } },
        .{ .key = "missing", .val = .{ .int = 7 } },
        .{ .key = "assert", .val = .{ .int = 8 } },
        .{ .key = "as", .val = .{ .int = 9 } },
        .{ .key = "Infinity", .val = .{ .int = 10 } },
        .{ .key = "NaN", .val = .{ .int = 11 } },
        .{ .key = "merge", .val = .{ .int = 12 } },
        .{ .key = "Some", .val = .{ .int = 13 } },
        .{ .key = "toMap", .val = .{ .int = 14 } },
        .{ .key = "forall", .val = .{ .int = 15 } },
        .{ .key = "with", .val = .{ .int = 16 } },
        .{ .key = "ordinary", .val = .{ .int = 17 } },
    }};
    _ = my_data;
}
