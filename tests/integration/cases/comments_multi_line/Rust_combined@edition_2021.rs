fn main() {
    let mut my_data = vec![
        // line 1
        // line 2
        "a",
    ];
    let _ = &my_data;
    my_data = vec![
        // line 1
        // line 2
        "a",
    ];
    let _ = &mut my_data;
}
