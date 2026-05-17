fn process(data: anytype, count: anytype) void { _ = data; _ = count; }
pub fn main() void {
    const my_ints = &.{
        1,
        2,
        3,
    };
    const my_strings = &.{
        "a",
        "b",
    };
    const my_empty = &.{};
    process(my_ints, 42);
    process(my_strings, 7);
    process(my_empty, 99);
}
