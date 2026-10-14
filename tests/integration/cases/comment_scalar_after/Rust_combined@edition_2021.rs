fn main() {
    // after
    let mut my_data = 42;
    let _ = &my_data;
    // after
    my_data = 42;
    let _ = &mut my_data;
}
