const Record0 = struct { id: i64 };
pub fn main() void {
    var shared = &.{
        Record0{ .id = 1 },
    };
    var second = &.{
        Record0{ .id = 2 },
    };
    var my_data: []const []const Record0 = &.{
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
