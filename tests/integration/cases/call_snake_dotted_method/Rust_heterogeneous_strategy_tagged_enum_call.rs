enum Value {
    Str(&'static str),
    I32(i32),
    Bool(bool),
}
fn main() {
    struct Http_ClientType_;
    impl Http_ClientType_ { fn fetch<A>(&self, _payload: A) {} }
    struct My_AppType_ { http_client: Http_ClientType_ }
    let my_app = My_AppType_ { http_client: Http_ClientType_ };
    my_app.http_client.fetch("hello");
    my_app.http_client.fetch(42);
    my_app.http_client.fetch(true);
}
