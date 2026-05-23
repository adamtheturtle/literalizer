#include <nlohmann/json.hpp>
int main() {
nlohmann::json my_data = nlohmann::json::parse(R"json({"date": "2024-01-15", "datetime": "2024-01-15T12:30:00+00:00"})json");
    (void)my_data;
    return 0;
}
