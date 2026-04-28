#include <initializer_list>
#include <string>
auto main() -> int {
auto my_data = std::initializer_list<std::string>{
    "2024-01-15",
    "2024-06-01",
};
    (void)my_data;
    return 0;
}
