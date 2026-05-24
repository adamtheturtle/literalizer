#include <nlohmann/json.hpp>
int main() {
auto my_data = nlohmann::json::parse(R"json([[1, "a"], [2, "b"]])json", nullptr, false);
    (void)my_data;
    return 0;
}
