fn main() {
    #[allow(unused_mut)]
    let mut my_data = -9223372036854775808i64;
    let _ = &my_data;
    my_data = -9223372036854775808i64;
    let _ = &mut my_data;
}
