fn main() {
    fn make_widget<A>(_count: A) {}
    static my_data: i32 = 42;
    my_data = (~/\//).match("/") ? make_widget(42) : null // trailing;
}
