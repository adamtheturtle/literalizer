fn main() {
    // note
    let mut my_data = None::<()>;
    let _ = &my_data;
    // note
    my_data = None::<()>;
    let _ = &mut my_data;
}
