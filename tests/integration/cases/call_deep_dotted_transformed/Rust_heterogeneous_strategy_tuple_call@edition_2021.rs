#[allow(non_snake_case)]
fn main() {
    struct ClientType;
    impl ClientType { fn fetch<A>(&self, _payload: A) {} }
    struct AppType { client: ClientType }
    let app = AppType { client: ClientType };
    fn emit<A>(__arg: A) {}
    emit(app.client.fetch("hello"));
    emit(app.client.fetch(42));
    emit(app.client.fetch(true));
}
