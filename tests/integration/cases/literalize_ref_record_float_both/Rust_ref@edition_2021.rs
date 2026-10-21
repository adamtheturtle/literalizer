fn main() {
    let mut first = 3.5;
    let mut my_data = first;
    let _ = &my_data;
    my_data = first;
    let _ = &mut my_data;
    let _ = &mut first;
}
