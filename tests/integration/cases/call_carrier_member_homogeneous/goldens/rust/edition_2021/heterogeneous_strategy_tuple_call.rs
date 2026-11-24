fn main() {
    struct AppType;
    impl AppType { fn go<A, B>(&self, _first_value: A, _second_value: B) {} }
    let app = AppType;
    app.go(vec![1], vec![2]);
}
