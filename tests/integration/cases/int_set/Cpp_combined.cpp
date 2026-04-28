#include <initializer_list>
auto main() -> int {
auto my_data = std::initializer_list<int>{
    1,
    2,
    3,
};
(void)my_data;
my_data = std::initializer_list<int>{
    1,
    2,
    3,
};
    (void)my_data;
    return 0;
}
