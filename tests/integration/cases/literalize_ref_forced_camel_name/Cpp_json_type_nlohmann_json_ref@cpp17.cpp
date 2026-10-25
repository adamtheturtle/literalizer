#include <nlohmann/json.hpp>
#include <utility>
int main() {
    try {
auto userObj = nlohmann::json::object({
    {"_", "_"},
});
auto&& my_data = std::move(userObj);
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
