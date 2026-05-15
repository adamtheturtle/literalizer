fn main() {
    struct ClientType_;
    impl ClientType_ { fn fetch<A>(&self, _payload: A) {} }
    struct AppType_ { client: ClientType_ }
    let app = AppType_ { client: ClientType_ };
    fn emit<A>(__arg: A) {}
    emit(app.client.fetch("hello"));
    emit(app.client.fetch(42));
    emit(app.client.fetch(true));
}
