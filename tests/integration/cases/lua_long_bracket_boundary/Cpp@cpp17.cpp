#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    "]",
    "a]",
    "a]=",
    "a]b",
};
    (void)my_data;
    return 0;
}
