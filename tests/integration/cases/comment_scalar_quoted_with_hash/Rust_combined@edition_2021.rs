fn main() {
    // note
    let mut my_data = "hello # world";
    let _ = &my_data;
    // note
    my_data = "hello # world";
    let _ = &mut my_data;
}
