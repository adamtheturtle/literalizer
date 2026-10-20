pub fn main() void {
    var first = true;
    var my_data = first;
    my_data = first;
    _ = &first;
    _ = &my_data;
}
