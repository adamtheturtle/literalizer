#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct http_clientType_ { template <typename... Args> void fetch(Args...) const {} };
struct my_appType_ { http_clientType_ http_client; };
const my_appType_ my_app;
int main() {
my_app.http_client.fetch("hello");
my_app.http_client.fetch(42);
my_app.http_client.fetch(true);
    return 0;
}
