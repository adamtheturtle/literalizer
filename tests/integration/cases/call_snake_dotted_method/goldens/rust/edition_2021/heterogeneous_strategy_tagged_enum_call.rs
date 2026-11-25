fn main() {
    struct HttpClientType;
    impl HttpClientType { fn fetch<A>(&self, _payload: A) {} }
    struct MyAppType { http_client: HttpClientType }
    let my_app = MyAppType { http_client: HttpClientType };
    my_app.http_client.fetch("hello");
    my_app.http_client.fetch(42);
    my_app.http_client.fetch(true);
}
