#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    // line 1
    // line 2
    "a",
};
(void)my_data;
my_data = std::vector<std::string>{
    // line 1
    // line 2
    "a",
};
    (void)my_data;
    return 0;
}
