#include <nlohmann/json.hpp>
#include <utility>
int main() {
    try {
auto shared = nlohmann::json::array({
    1,
    2,
});
auto build = nlohmann::json::array({
    1,
    2,
});
auto json_object = nlohmann::json::array({
    1,
    2,
});
auto json_allocator = nlohmann::json::array({
    1,
    2,
});
auto json_entries = nlohmann::json::array({
    1,
    2,
});
auto json_entry = nlohmann::json::array({
    1,
    2,
});
auto my_data = nlohmann::json::object({
    {"field", shared},
    {"nested", nlohmann::json::array({shared, nlohmann::json::object({})})},
    {"build", std::move(build)},
    {"json_object", std::move(json_object)},
    {"json_allocator", std::move(json_allocator)},
    {"json_entries", std::move(json_entries)},
    {"json_entry", std::move(json_entry)},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
