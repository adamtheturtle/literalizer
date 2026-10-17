fn main() {
    fn consume_widget<A>(__arg: A) {}
    let ref_data = vec![
        1,
        2,
    ];
    let my_data = vec![
        0,
    ];
    consume_widget(my_data);
    my_data = ref_data;
    consume_widget(my_data);
}
