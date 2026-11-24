#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json("hello \"world\" -- not a comment");
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
