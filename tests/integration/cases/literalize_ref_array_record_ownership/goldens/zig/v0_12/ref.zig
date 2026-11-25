const Record1 = struct { values: []const i64 };
const Record2 = struct { nested: []const []const i64 };
const Record0 = struct { trivial: Record1, nested: Record2 };
pub fn main() void {
    const trivial = Record1{
        .values = &.{
            1,
            2,
        },
    };
    const nested = Record2{
        .nested = &.{
            &.{
                1,
                2,
            },
            &.{
                3,
                4,
            },
        },
    };
    const my_data = Record0{
        .trivial = trivial,
        .nested = nested,
    };
    _ = my_data;
}
