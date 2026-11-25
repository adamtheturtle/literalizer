fn main() {
    fn make_widget<A, B, C>(_before: A, _populated: B, _after: C) {}
    make_widget(Vec::<String>::new(), vec![1], Vec::<String>::new());
    make_widget(vec!["text"], vec![2], Vec::<String>::new());
    make_widget(Vec::<String>::new(), vec!["text"], Vec::<String>::new());
    make_widget(vec!["text"], vec![2], vec![3]);
}
