#include <nlohmann/json.hpp>
int main() {
nlohmann::json my_data = nlohmann::json::parse(R"json([[1, "a"], [2, "b"]])json");
    (void)my_data;
    return 0;
}
