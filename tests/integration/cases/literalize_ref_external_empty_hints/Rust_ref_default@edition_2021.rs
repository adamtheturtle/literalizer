fn main() {
    fn consume_widget<A>(_arg_value: A) {}
    let item = vec![
        1,
        2,
    ];
    let mut my_data = vec![
        1,
        2,
    ];
    consume_widget(my_data);
    my_data = item;
    consume_widget(my_data);
}
