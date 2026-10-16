fn make_widget(before: anytype, populated: anytype, after: anytype) i64 { _ = before; _ = populated; _ = after; return 0; }
pub fn main() void {
    make_widget(&.{}, &.{1}, &.{});
    make_widget(&.{"text"}, &.{2}, &.{});
    make_widget(&.{}, &.{"text"}, &.{});
    make_widget(&.{"text"}, &.{2}, &.{3});
}
