#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    "a b c",
    "a\r b",
};
    (void)my_data;
    return 0;
}
