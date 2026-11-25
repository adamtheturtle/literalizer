const Record0 = struct { a: i64 };
pub fn main() void {
    const ZVal = Record0{
        .a = 1,
    };
    const ZKV = Record0{
        .a = 2,
    };
    const my_data = &.{
        ZVal,
        ZKV,
    };
    _ = my_data;
}
