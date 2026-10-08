const Record1 = struct { value: i64 };
const Record0 = struct { child: Record1 };
pub fn main() void {
    const first = Record0{
        .child = Record1{
            .value = 1,
        },
    };
    const my_data = first;
    _ = my_data;
}
