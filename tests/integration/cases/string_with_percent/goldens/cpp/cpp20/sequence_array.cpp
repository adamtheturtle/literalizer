#include <array>
#include <string>
int main() {
auto my_data = std::array<std::string, 2>{
    "100% done",
    "%(name) is here",
};
    (void)my_data;
    return 0;
}
