fn main() {
    fn consume_widget<A>(__arg: A) {}
    let item = None::<()>;
    let my_data = None::<()>;
    consume_widget(my_data);
    my_data = item;
    consume_widget(my_data);
}
