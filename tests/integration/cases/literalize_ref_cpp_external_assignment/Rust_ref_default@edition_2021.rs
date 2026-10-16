fn main() {
    let ref_data = vec![
        1,
        2,
    ];
    let my_data = vec![
        0,
    ];
    (void)my_data;
    my_data = ref_data;
    (void)my_data;
}
