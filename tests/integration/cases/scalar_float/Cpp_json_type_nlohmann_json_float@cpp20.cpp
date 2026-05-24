#include <nlohmann/json.hpp>
int main() {
auto my_data = nlohmann::json::parse(R"json(3.14)json", nullptr, false);
    (void)my_data;
    return 0;
}
