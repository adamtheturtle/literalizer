#include <initializer_list>
int main() {
auto my_data = std::initializer_list<int>{
    1,
    1099511627776,
};
(void)my_data;
my_data = std::initializer_list<int>{
    1,
    1099511627776,
};
    (void)my_data;
    return 0;
}
