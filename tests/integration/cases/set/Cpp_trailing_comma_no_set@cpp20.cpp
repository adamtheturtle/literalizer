#include <initializer_list>
#include <string>
int main() {
auto my_data = std::initializer_list<std::string>{
    "apple",
    "banana",
    "cherry"
};
    (void)my_data;
    return 0;
}
