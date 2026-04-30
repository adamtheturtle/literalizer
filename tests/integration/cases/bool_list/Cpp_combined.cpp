#include <initializer_list>
#include <vector>
int main() {
const auto my_data = std::vector<bool>{
    true,
    false,
    true,
};
(void)my_data;
my_data = std::vector<bool>{
    true,
    false,
    true,
};
    (void)my_data;
    return 0;
}
