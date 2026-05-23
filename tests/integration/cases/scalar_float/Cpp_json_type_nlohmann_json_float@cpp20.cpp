#include <nlohmann/json.hpp>
int main() {
nlohmann::json my_data = nlohmann::json::parse(R"json(3.14)json");
    (void)my_data;
    return 0;
}
