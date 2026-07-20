#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    "café",
    "中文",
};
(void)my_data;
my_data = std::vector<std::string>{
    "café",
    "中文",
};
    (void)my_data;
    return 0;
}
