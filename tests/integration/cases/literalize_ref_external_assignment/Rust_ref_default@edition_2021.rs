fn main() {
    fn consume_widget<A>(_arg_value: A) {}
    let ref_data = vec![
        1,
        2,
    ];
    let mut my_data = vec![
        0,
    ];
    consume_widget(my_data.clone());
    my_data = ref_data;
    consume_widget(my_data.clone());
}
