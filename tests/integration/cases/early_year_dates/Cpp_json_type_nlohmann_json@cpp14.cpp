#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"date", "0099-05-27"},
    {"naive", "0001-01-01T12:30:00"},
    {"recent", "2024-05-27T10:00:00"},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
