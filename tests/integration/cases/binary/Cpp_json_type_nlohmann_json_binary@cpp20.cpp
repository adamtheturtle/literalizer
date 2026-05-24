#include <nlohmann/json.hpp>
int main() {
auto my_data = nlohmann::json::parse(R"json(["48656c6c6f"])json", nullptr, false);
    (void)my_data;
    return 0;
}
