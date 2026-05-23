#include <nlohmann/json.hpp>
int main() {
nlohmann::json my_data = nlohmann::json::parse(R"json(["48656c6c6f"])json");
    (void)my_data;
    return 0;
}
