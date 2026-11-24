pub fn main() void {
    var my_data: []const []const []const u8 = &.{
        &.{},
        &.{"one", "two"},
    };
    _ = &my_data;
}
