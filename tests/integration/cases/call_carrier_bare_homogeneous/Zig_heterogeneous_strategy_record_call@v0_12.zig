fn make_widget(first_value: anytype, second_value: anytype) void { _ = first_value; _ = second_value; }
pub fn main() void {
    make_widget(&.{1}, &.{2});
}
