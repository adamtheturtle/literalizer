#include <nlohmann/json.hpp>
int main() {
nlohmann::json my_data = nlohmann::json::parse(R"json({"starts_at": "09:30:00"})json");
    (void)my_data;
    return 0;
}
