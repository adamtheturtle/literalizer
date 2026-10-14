fn main() {
    // note
    let mut my_data = 42;
    let _ = &my_data;
    // note
    my_data = 42;
    let _ = &mut my_data;
}
