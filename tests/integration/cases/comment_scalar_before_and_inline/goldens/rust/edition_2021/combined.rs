fn main() {
    // inline
    let mut my_data = // before
    "plain";
    let _ = &my_data;
    // inline
    my_data = // before
    "plain";
    let _ = &mut my_data;
}
