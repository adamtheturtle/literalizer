fn make_widget(value: anytype) i64 { _ = value; return 0; }
pub fn main() void {
    const items = &.{};
    make_widget(items);
}
