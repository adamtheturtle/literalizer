#include <initializer_list>
#include <string>
#include <vector>
#include <variant>
struct apiType_ { [[nodiscard]] auto request(auto...) const { return 0; } };
struct clientType_ { apiType_ api; };
const clientType_ client;
void check_() {
client.api.request("hello");
client.api.request(42);
client.api.request(true);
}
