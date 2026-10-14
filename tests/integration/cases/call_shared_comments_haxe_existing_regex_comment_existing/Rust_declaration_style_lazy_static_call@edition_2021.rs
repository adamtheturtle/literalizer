use std::sync::LazyLock;
fn main() {
    fn make_widget<A>(_count: A) {}
    let mut my_data = make_widget(42);
    my_data = (~/\//).match("/") ? make_widget(42) : null // trailing;
}
