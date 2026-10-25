fn main() {
    let mut first = 42;
    let _ = &mut first;
    let mut my_data = first;
    let _ = &my_data;
    my_data = first;
    let _ = &mut my_data;
}
