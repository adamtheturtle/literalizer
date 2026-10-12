use std::sync::LazyLock;
fn main() {
    fn make_widget<A>(_count: A) {}
    static my_data: LazyLock<i32> = LazyLock::new(|| 42);
    my_data = (~/\//).match("/") ? make_widget(42) : null // trailing;
}
