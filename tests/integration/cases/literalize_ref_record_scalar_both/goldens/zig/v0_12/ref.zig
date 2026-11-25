pub fn main() void {
    var first: i64 = 42;
    var my_data: i64 = first;
    my_data = first;
    _ = &first;
    _ = &my_data;
}
