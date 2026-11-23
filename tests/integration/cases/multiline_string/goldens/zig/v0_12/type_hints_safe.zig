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
    const my_data: ZVal = .{ .arr = &.{
        .{ .str = "first line\n  indented\n\nlast line" },
        .{ .str = "\nleading newline" },
        .{ .str = " \t\nleading whitespace" },
        .{ .str = "trailing newline\n" },
        .{ .str = "\nleading and trailing\n" },
        .{ .str = "quotes: \"\"\" ''' ` and backslash: \\" },
        .{ .str = "interpolation: ${value} #{value} #@value #$value $value" },
        .{ .str = "backslash before newline: \\\nnext line" },
        .{ .str = "trailing spaces  \nnext" },
        .{ .str = "C++ empty delimiter collision: )\"\nvalue" },
        .{ .str = "C++ first fallback collision: )\" and )x\"\nvalue" },
        .{ .str = "C++ second fallback collision: )\" and )x\" and )x0\"\nvalue" },
        .{ .str = "Rust delimiter collision: \"#\nvalue" },
        .{ .str = "Lua delimiter collision: ]]\nvalue" },
        .{ .str = "Swift delimiter collision: \"\"\"#\nvalue" },
        .{ .str = "Swift interpolation collision: \\#(value)\nvalue" },
        .{ .str = "Ruby fallback interpolation  \n#{expression} #@instance #$global" },
        .{ .str = "NUL followed by a digit: \x007" },
        .{ .str = "carriage\rreturn" },
    }};
    _ = my_data;
}
