fn main() {
    struct ClientType;
    impl ClientType { fn go<A, B>(&self, _first_value: A, _second_value: B) {} }
    struct AppType { client: ClientType }
    let app = AppType { client: ClientType };
    app.client.go(vec![Value::I32(1)], vec![Value::Str("text")]);
}
