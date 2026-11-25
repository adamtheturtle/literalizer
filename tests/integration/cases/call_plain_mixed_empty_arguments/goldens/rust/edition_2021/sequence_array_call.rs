fn main() {
    fn make_widget<A, B, C>(_before: A, _populated: B, _after: C) {}
    make_widget([] as [String; 0], [1], [] as [String; 0]);
    make_widget(["text"], [2], [] as [String; 0]);
    make_widget([] as [String; 0], ["text"], [] as [String; 0]);
    make_widget(["text"], [2], [3]);
}
