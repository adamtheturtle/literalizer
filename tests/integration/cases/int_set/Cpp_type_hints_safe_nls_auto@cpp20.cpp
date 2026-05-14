#include <initializer_list>
int main() {
auto my_data = std::initializer_list<long>{
    1L,
    2L,
    3L,
};
    (void)my_data;
    return 0;
}
