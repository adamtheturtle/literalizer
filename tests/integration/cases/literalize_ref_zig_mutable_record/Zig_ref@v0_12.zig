pub fn main() void {
    var shared = &.{
        1,
        2,
    };
    var my_data = shared;
    _ = &shared;
    _ = &my_data;
}
