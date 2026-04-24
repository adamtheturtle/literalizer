#include <initializer_list>
void check_() {
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
}
