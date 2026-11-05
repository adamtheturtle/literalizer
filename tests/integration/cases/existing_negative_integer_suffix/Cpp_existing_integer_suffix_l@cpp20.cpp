
#include <type_traits>
int main() {
auto my_data = -0x80000000LL;
    static_assert(std::is_same<decltype(my_data), long long>::value,
                  "the composed literal must retain its signed LL type");
    return my_data == -2147483648LL ? 0 : 1;
}
