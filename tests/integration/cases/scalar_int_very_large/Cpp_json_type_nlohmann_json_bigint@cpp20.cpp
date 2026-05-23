#include <nlohmann/json.hpp>
int main() {
nlohmann::json my_data = nlohmann::json::parse(R"json(9223372036854775808)json");
    (void)my_data;
    return 0;
}
