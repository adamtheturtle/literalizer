fn main() {
    fn make_widget<A>(_count: A) {}
    let my_data = ('prefix ${'// payload'}').length >= 0 ? make_widget(42) : make_widget(42);
    let _ = my_data;
}
