fn main() {
    struct ClientType_;
    impl ClientType_ { fn send<A>(&self, _payload: A) {} }
    struct NsType_ { client: ClientType_ }
    let ns = NsType_ { client: ClientType_ };
    ns.client.send("hello");
    ns.client.send(42);
    ns.client.send(true);
}
