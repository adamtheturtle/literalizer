#include <initializer_list>
#include <string>
#include <vector>
int main() {
const auto my_data = std::vector<std::string>{
    "price $10",
    "$HOME",
};
(void)my_data;
my_data = std::vector<std::string>{
    "price $10",
    "$HOME",
};
    (void)my_data;
    return 0;
}
