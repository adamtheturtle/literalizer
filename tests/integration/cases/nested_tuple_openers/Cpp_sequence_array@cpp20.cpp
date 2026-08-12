#include <initializer_list>
#include <array>
int main() {
auto my_data = {
    {{std::array<int, 1>{1}}},
};
    (void)my_data;
    return 0;
}
