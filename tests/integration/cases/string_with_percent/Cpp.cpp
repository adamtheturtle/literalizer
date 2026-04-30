#include <initializer_list>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::string>{
    "100% done",
    "%(name) is here",
};
    (void)my_data;
    return 0;
}
