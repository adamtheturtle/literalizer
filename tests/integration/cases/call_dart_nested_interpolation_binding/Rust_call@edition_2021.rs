fn main() {
    fn make_widget<A>(_count: A) {}
    let my_data = "${"${"// payload"}"}" // trailing
    // extra;
    let _ = my_data;
}
