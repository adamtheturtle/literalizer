pub fn main() void {
    var my_data: []const []const []const u8 = &.{
        &.{},
        &.{"one", "two"},
    };
    my_data = &.{
        &.{},
        &.{"one", "two"},
    };
    _ = &my_data;
}
