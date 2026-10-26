#include <array>
#include <string>
int main() {
auto my_data = std::array<std::string, 2>{
    "prefix ${HOME} suffix",
    "${interpolated}",
};
    (void)my_data;
    return 0;
}
