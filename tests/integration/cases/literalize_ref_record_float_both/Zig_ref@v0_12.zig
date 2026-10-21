pub fn main() void {
    var first: f64 = 3.5;
    var my_data: f64 = first;
    my_data = first;
    _ = &first;
    _ = &my_data;
}
