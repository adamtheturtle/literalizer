const Record2 = struct { value: i64 };
const Record1 = struct { items: struct { i64, Record2 } };
const Record4 = struct { value: []const u8 };
const Record3 = struct { items: struct { i64, Record4 } };
const Record0 = struct { first: Record1, second: Record3 };
pub fn main() void {
    const my_data = Record0{
        .first = Record1{
            .items = .{
                1,
                Record2{
                    .value = 2,
                },
            },
        },
        .second = Record3{
            .items = .{
                1,
                Record4{
                    .value = "s",
                },
            },
        },
    };
    _ = my_data;
}
