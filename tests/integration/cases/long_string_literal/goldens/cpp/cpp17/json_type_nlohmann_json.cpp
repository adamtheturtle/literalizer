#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json::object({
    {"long_str", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"},
    {"quoted", "a\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"ba\"b"},
    {"wide", "中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中"},
});
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
