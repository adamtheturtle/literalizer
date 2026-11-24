const Record1 = struct { x: i64 };
const Record2 = struct { day: i64, stamp: i64 };
const Record0 = struct { plain: Record1, timed: Record2 };
pub fn main() void {
    const plain = Record1{
        .x = 1,
    };
    const timed = Record2{
        .day = 978393600,
        .stamp = 978404645,
    };
    const my_data = Record0{
        .plain = plain,
        .timed = timed,
    };
    _ = my_data;
}
