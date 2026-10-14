fn main() {
    #[allow(unused_mut)]
    let mut my_data = "hello";
    let _ = &my_data;
    my_data = "hello";
    let _ = &mut my_data;
}
