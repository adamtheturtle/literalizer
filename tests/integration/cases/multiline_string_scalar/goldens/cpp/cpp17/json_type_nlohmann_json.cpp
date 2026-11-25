#include <nlohmann/json.hpp>
int main() {
    try {
auto my_data = nlohmann::json("\nroot first line\n  indented\n\nroot last line\n");
    (void)my_data;
        return 0;
    } catch (...) {
        return 1;
    }
}
