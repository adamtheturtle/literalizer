#include <vector>
#include <string>
int main() {
static auto my_data = std::vector<std::string>{
    "apple",
    "banana",
    "cherry",
};
    (void)my_data;
    return 0;
}
