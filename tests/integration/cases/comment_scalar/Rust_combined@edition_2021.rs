fn main() {
    #[allow(unused_mut)]
    let mut my_data = // note
    42;
    let _ = &my_data;
    my_data = // note
    42;
    let _ = &mut my_data;
}
