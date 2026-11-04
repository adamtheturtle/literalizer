fn main() {
    fn make_widget<A, B, C>(_before: A, _populated: B, _after: C) {}
    make_widget((), (1,), ());
    make_widget(("text",), (2,), ());
    make_widget((), ("text",), ());
    make_widget(("text",), (2,), (3,));
}
