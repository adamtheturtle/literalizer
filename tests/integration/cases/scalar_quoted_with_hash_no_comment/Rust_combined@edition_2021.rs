fn main() {
    let mut my_data = "hello # world";
    let _ = &my_data;
    my_data = "hello # world";
    let _ = &mut my_data;
}
