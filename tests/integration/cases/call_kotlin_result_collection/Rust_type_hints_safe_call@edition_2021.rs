fn main() {
    fn make_widget<A>(_items: A) {}
    let my_data = make_widget(vec![vec![1, 2], vec![3]]);
    let _ = my_data;
}
