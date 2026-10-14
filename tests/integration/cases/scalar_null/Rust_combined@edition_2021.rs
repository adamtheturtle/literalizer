fn main() {
    #[allow(unused_mut)]
    let mut my_data = None::<()>;
    let _ = &my_data;
    my_data = None::<()>;
    let _ = &mut my_data;
}
