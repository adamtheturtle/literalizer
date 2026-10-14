fn main() {
    #[allow(unused_mut)]
    let mut my_data = Vec::<String>::new();
    let _ = &my_data;
    my_data = Vec::<String>::new();
    let _ = &mut my_data;
}
