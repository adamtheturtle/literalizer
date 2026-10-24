#include <initializer_list>
#include <string>
#include <array>
int main() {
auto my_data = std::array<std::string, 2>{
    "100% done",
    "%(name) is here",
};
    (void)my_data;
    return 0;
}
