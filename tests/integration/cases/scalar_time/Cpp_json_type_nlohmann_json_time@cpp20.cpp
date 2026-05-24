#include <nlohmann/json.hpp>
int main() {
auto my_data = nlohmann::json::parse(R"json({"starts_at": "09:30:00"})json", nullptr, false);
    (void)my_data;
    return 0;
}
