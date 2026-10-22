fn main() {
    fn make_widget<A>(_value: A) {}
    fn consume<A>(_value: A) {}
    let my_data = {
        make_widget(42);
        {
            fn make_widget<'a>() where 'a: 'a {}
            make_widget::<'static>()
        }
    }; // note
    consume(my_data);
}
