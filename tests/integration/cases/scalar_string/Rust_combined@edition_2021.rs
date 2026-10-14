fn main() {
    let mut my_data = "hello";
    let _ = &my_data;
    my_data = "hello";
    let _ = &mut my_data;
}
