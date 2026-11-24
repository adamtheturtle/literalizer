const Record1 = struct { x: i64, y: ?i64 };
const Record2 = struct { x: ?i64, y: ?i64 };
const Record3 = struct { x: i64, y: i64 };
const Record0 = struct { nullable: Record1, null_fields: Record2, plain: Record3 };
pub fn main() void {
    const nullable = Record1{
        .x = 1,
        .y = null,
    };
    const null_fields = Record2{
        .x = null,
        .y = null,
    };
    const plain = Record3{
        .x = 1,
        .y = 2,
    };
    const my_data = Record0{
        .nullable = nullable,
        .null_fields = null_fields,
        .plain = plain,
    };
    _ = my_data;
}
