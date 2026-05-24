#include <nlohmann/json.hpp>
int main() {
auto my_data = nlohmann::json::parse(R"json(2147483648)json", nullptr, false);
    (void)my_data;
    return 0;
}
