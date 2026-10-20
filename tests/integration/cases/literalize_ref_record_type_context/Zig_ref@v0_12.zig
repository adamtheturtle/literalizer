const Record1 = struct { x: []const u8 };
const Record2 = struct { x: i64 };
const Record0 = struct { direct: Record1, bound: Record2 };
pub fn main() void {
    const first = Record2{
        .x = 1,
    };
    const my_data = Record0{
        .direct = Record1{
            .x = "s",
        },
        .bound = first,
    };
    _ = my_data;
}
