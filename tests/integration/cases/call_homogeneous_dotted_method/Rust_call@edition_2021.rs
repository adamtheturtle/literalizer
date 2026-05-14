fn main() {
    struct ClientType_;
    impl ClientType_ { fn fetch<A>(&self, _value: A) {} }
    struct AppType_ { client: ClientType_ }
    let app = AppType_ { client: ClientType_ };
    app.client.fetch("hello");
    app.client.fetch("world");
}
