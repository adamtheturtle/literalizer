const Record0 = struct { a: i64, b: []const u8 };
fn consume_widget(arg_value: anytype) void { _ = arg_value; }
pub fn main() void {
    consume_widget(Record0{
        .a = 1,
        .b = "x",
    });
}
