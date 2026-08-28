#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::parse(R"json({
    "$key": "a\"b\tcé #{world} $ident",
    "trailing multi-byte": "café"
})json");
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
