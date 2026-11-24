fn main() {
    let mut my_data = -2147483649i64;
    let _ = &my_data;
    my_data = -2147483649i64;
    let _ = &mut my_data;
}
