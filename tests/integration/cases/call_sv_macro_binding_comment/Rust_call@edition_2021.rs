fn main() {
    fn make_widget<A>(_count: A) {}
    let my_data = (`__LINE__ > 0) ? make_widget(42) : make_widget(42) // trailing `marker;
    let _ = my_data;
}
