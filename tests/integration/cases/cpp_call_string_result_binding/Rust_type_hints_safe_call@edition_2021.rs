fn main() {
    fn make_widget<A>(_text: A) {}
    let my_data = make_widget("text");
    let _ = my_data;
}
