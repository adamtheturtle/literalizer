fn main() {
    fn consume_widget<A>(_arg_value: A) {}
    let item = None::<()>;
    let mut my_data = None::<()>;
    consume_widget(my_data);
    my_data = item;
    consume_widget(my_data);
}
