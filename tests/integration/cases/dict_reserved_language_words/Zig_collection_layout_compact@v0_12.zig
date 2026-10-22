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
        .{ .key = "assert", .val = .{ .int = 1 } },
        .{ .key = "else", .val = .{ .int = 1 } },
        .{ .key = "error", .val = .{ .int = 1 } },
        .{ .key = "false", .val = .{ .int = 1 } },
        .{ .key = "for", .val = .{ .int = 1 } },
        .{ .key = "function", .val = .{ .int = 1 } },
        .{ .key = "if", .val = .{ .int = 1 } },
        .{ .key = "import", .val = .{ .int = 1 } },
        .{ .key = "importbin", .val = .{ .int = 1 } },
        .{ .key = "importstr", .val = .{ .int = 1 } },
        .{ .key = "in", .val = .{ .int = 1 } },
        .{ .key = "local", .val = .{ .int = 1 } },
        .{ .key = "null", .val = .{ .int = 1 } },
        .{ .key = "self", .val = .{ .int = 1 } },
        .{ .key = "super", .val = .{ .int = 1 } },
        .{ .key = "tailstrict", .val = .{ .int = 1 } },
        .{ .key = "then", .val = .{ .int = 1 } },
        .{ .key = "true", .val = .{ .int = 1 } },
        .{ .key = "ordinary", .val = .{ .int = 1 } },
    }};
    _ = my_data;
}
