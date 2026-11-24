fn make_widget(value: anytype) i64 { _ = value; return 0; }
pub fn main() void {
    const my_data = make_widget(&.{});
    _ = my_data;
}
