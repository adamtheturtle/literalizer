fn main() {
    let mut my_data = vec![
        // outer heading
        // first empty
        Vec::<String>::new(),
        // second empty
        Vec::<String>::new(),
    ];
    let _ = &my_data;
    my_data = vec![
        // outer heading
        // first empty
        Vec::<String>::new(),
        // second empty
        Vec::<String>::new(),
    ];
    let _ = &mut my_data;
}
