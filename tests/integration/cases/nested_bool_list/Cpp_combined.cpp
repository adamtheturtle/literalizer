#include <initializer_list>
#include <vector>
int main() {
auto my_data = std::vector<std::vector<bool>>{
    std::vector<bool>{true, false},
    std::vector<bool>{true, true},
};
(void)my_data;
my_data = std::vector<std::vector<bool>>{
    std::vector<bool>{true, false},
    std::vector<bool>{true, true},
};
    (void)my_data;
    return 0;
}
