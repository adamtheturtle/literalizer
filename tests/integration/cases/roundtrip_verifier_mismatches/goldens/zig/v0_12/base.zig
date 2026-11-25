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
        .{ .key = "true_to_one", .val = .{ .map = &.{.{ .key = "value", .val = .{ .int = 1 } }}} },
        .{ .key = "one_to_true", .val = .{ .map = &.{.{ .key = "value", .val = .{ .bool = true } }}} },
        .{ .key = "false_to_zero", .val = .{ .map = &.{.{ .key = "value", .val = .{ .int = 0 } }}} },
        .{ .key = "zero_to_false", .val = .{ .map = &.{.{ .key = "value", .val = .{ .bool = false } }}} },
        .{ .key = "nested_boolean_to_float", .val = .{ .map = &.{.{ .key = "value", .val = .{ .arr = &.{.{ .float = 1.0 }}} }}} },
        .{ .key = "nested_float_to_boolean", .val = .{ .map = &.{.{ .key = "value", .val = .{ .arr = &.{.{ .bool = false }}} }}} },
        .{ .key = "nested_value_types_changed", .val = .{ .map = &.{.{ .key = "value", .val = .{ .map = &.{.{ .key = "nested", .val = .{ .arr = &.{.{ .bool = true }, .{ .int = 0 }}} }}} }}} },
        .{ .key = "nested_value_types_reversed", .val = .{ .map = &.{.{ .key = "value", .val = .{ .map = &.{.{ .key = "nested", .val = .{ .arr = &.{.{ .int = 1 }, .{ .bool = false }}} }}} }}} },
        .{ .key = "array_order_changed", .val = .{ .map = &.{.{ .key = "value", .val = .{ .arr = &.{.{ .int = 2 }, .{ .int = 1 }}} }}} },
        .{ .key = "array_length_changed", .val = .{ .map = &.{.{ .key = "value", .val = .{ .arr = &.{.{ .int = 1 }, .{ .int = 2 }}} }}} },
        .{ .key = "null_to_zero", .val = .{ .map = &.{.{ .key = "value", .val = .{ .int = 0 } }}} },
        .{ .key = "string_to_boolean", .val = .{ .map = &.{.{ .key = "value", .val = .{ .bool = true } }}} },
        .{ .key = "object_key_changed", .val = .{ .map = &.{.{ .key = "value", .val = .{ .map = &.{.{ .key = "b", .val = .{ .int = 1 } }}} }}} },
    }};
    _ = my_data;
}
