fn main() {
    let mut my_data = 42;
    let _ = &my_data;
    my_data = 42;
    let _ = &mut my_data;
}
