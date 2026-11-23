const std = @import("std");
pub fn main() void {
    var @"JSON arena" = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer @"JSON arena".deinit();
    const allocator = @"JSON arena".allocator();
    const my_data = (std.json.parseFromSlice(std.json.Value, allocator, "[\"first line\\n  indented\\n\\nlast line\", \"\\nleading newline\", \" \\t\\nleading whitespace\", \"trailing newline\\n\", \"\\nleading and trailing\\n\", \"quotes: \\\"\\\"\\\" ''' ` and backslash: \\\\\", \"interpolation: ${value} #{value} #@value #$value $value\", \"backslash before newline: \\\\\\nnext line\", \"trailing spaces  \\nnext\", \"C++ empty delimiter collision: )\\\"\\nvalue\", \"C++ first fallback collision: )\\\" and )x\\\"\\nvalue\", \"C++ second fallback collision: )\\\" and )x\\\" and )x0\\\"\\nvalue\", \"Rust delimiter collision: \\\"#\\nvalue\", \"Lua delimiter collision: ]]\\nvalue\", \"Swift delimiter collision: \\\"\\\"\\\"#\\nvalue\", \"Swift interpolation collision: \\\\#(value)\\nvalue\", \"Ruby fallback interpolation  \\n#{expression} #@instance #$global\", \"NUL followed by a digit: \\u00007\", \"carriage\\rreturn\"]", .{}) catch unreachable).value;
    _ = my_data;
}
