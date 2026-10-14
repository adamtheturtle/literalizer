fn main() {
    let mut my_data = -9223372036854775809i128;
    let _ = &my_data;
    my_data = -9223372036854775809i128;
    let _ = &mut my_data;
}
