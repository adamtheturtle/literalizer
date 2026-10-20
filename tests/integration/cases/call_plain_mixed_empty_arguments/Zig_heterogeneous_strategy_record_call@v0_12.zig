fn make_widget(before: anytype, populated: anytype, after: anytype) i64 { _ = before; _ = populated; _ = after; return 0; }
pub fn main() void {
    _ = make_widget(&.{}, &.{1}, &.{});
    _ = make_widget(&.{"text"}, &.{2}, &.{});
    _ = make_widget(&.{}, &.{"text"}, &.{});
    _ = make_widget(&.{"text"}, &.{2}, &.{3});
}
