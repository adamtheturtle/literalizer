pub fn main() void {
    var shared = &.{
        1,
        2,
    };
    var second = "two";
    var my_data = .{
        shared,
        second,
    };
    my_data = .{
        shared,
        second,
    };
    _ = &shared;
    _ = &second;
    _ = &my_data;
}
