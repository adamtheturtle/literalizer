#include <nlohmann/json.hpp>
#include <limits>
int main() {
    try {
auto my_data = nlohmann::json::object({{"$key", "a\"b\tcé #{world} $ident"}});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
