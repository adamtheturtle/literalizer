fn main() {
    let mut first = true;
    let mut my_data = first;
    let _ = &my_data;
    my_data = first;
    let _ = &mut my_data;
    let _ = &mut first;
}
