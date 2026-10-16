fn make_widget(value: anytype) void { _ = value; }
pub fn main() void {
    make_widget(&.{});
}
