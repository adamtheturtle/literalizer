#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    "apple",
    "banana",
    "cherry",
};
    (void)my_data;
    return 0;
}
