#include <nlohmann/json.hpp>
int main() {
nlohmann::json my_data = nlohmann::json::parse(R"json("2024-01-15T12:30:00Z")json");
    (void)my_data;
    return 0;
}
