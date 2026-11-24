pub fn main() void {
    var shared = &.{
        1,
        2,
    };
    var second = &.{
        3,
        4,
    };
    var my_data: []const []const i64 = &.{
        shared,
        second,
    };
    my_data = &.{
        shared,
        second,
    };
    _ = &shared;
    _ = &second;
    _ = &my_data;
}
