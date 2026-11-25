fn process(data: anytype, count: anytype) void { _ = data; _ = count; }
pub fn main() void {
    const single_var = &.{
        4,
        5,
        6,
    };
    const repeated_var = 1;
    process(repeated_var, 1);
    process(single_var, 0);
    process(repeated_var, 8);
}
