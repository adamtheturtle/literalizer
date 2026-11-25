const Record1 = struct { integer: i64, boolean: bool, decimal: f64, null: ?i64 };
const Record3 = struct { integer: i64 };
const Record2 = struct { child: Record3 };
const Record4 = struct { text: []const u8 };
const Record5 = struct { day: i64, stamp: i64 };
const Record0 = struct { trivial: Record1, nested: Record2, owning: Record4, calendar: Record5 };
pub fn main() void {
    const trivial = Record1{
        .integer = 1,
        .boolean = true,
        .decimal = 1.5,
        .null = null,
    };
    const nested = Record2{
        .child = Record3{
            .integer = 2,
        },
    };
    const owning = Record4{
        .text = "owned",
    };
    const calendar = Record5{
        .day = 978393600,
        .stamp = 978404645,
    };
    const my_data = Record0{
        .trivial = trivial,
        .nested = nested,
        .owning = owning,
        .calendar = calendar,
    };
    _ = my_data;
}
