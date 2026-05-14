enum Value {
    Str(&'static str),
    I32(i32),
    Bool(bool),
}
fn main() {
    struct ClientType_;
    impl ClientType_ { fn fetch<A>(&self, _payload: A) {} }
    struct AppType_ { client: ClientType_ }
    let app = AppType_ { client: ClientType_ };
    app.client.fetch("hello");
    app.client.fetch(42);
    app.client.fetch(true);
}
