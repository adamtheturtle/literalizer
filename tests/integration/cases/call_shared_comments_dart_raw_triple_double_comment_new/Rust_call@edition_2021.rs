fn main() {
    fn make_widget<A>(_count: A) {}
    let my_data = (r"""ends\""" + "// payload").length >= 0 ? make_widget(42) : make_widget(42) // trailing
    // extra;
    let _ = &my_data;
}
