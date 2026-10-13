#[allow(non_snake_case)]
fn main() {
    struct ClientType;
    impl ClientType { fn fetch<A>(&self, _value: A) {} }
    struct AppType { client: ClientType }
    let app = AppType { client: ClientType };
    app.client.fetch("hello");
    app.client.fetch("world");
}
