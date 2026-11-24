pub fn main() void {
    var shared = &.{};
    var second = &.{
        "one",
        "two",
    };
    var my_data: []const []const []const u8 = &.{
        shared,
        second,
    };
    _ = &shared;
    _ = &second;
    _ = &my_data;
}
