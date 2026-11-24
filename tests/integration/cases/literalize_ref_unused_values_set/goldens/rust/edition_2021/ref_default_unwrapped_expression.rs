use std::collections::HashSet;
fn main() {
    fn consume_widget<A>(_arg_value: A) {}
    consume_widget(HashSet::from([
        1,
        2,
    ]));
}
