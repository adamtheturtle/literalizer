#include <nlohmann/json.hpp>
int main() {
nlohmann::json my_data = nlohmann::json::parse(R"json(2147483648)json");
    (void)my_data;
    return 0;
}
