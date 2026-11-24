pub fn main() void {
    var shared = &.{
        1,
        2,
    };
    var second = &.{
        "one",
        "two",
    };
    var my_data = .{
        shared,
        second,
    };
    _ = &shared;
    _ = &second;
    _ = &my_data;
}
