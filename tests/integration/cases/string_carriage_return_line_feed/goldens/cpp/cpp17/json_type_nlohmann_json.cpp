#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"cr", "a\rb"},
    {"crlf", "a\r\nb"},
    {"lf", "a\nb"},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
