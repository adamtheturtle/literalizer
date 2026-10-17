fn main() {
    fn consume_widget<A>(_arg_value: A) {}
    let shared = vec![
        1,
        2,
    ];
    let my_data = shared;
    consume_widget(my_data);
}
