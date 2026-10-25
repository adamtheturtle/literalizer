fn main() {
    fn consume_widget<A>(_arg_value: A) {}
    let shared = vec![
        1,
        2,
    ];
    let mut my_data = vec![
        0,
    ];
    consume_widget(my_data);
    my_data = shared;
    consume_widget(my_data);
}
