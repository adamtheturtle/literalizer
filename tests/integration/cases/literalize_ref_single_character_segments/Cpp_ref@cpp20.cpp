#include <initializer_list>
#include <string>
#include <map>
int main() {
auto a_b_c = std::map<std::string, std::string>{
    {"_", "_"},
};
auto my_data = std::move(a_b_c);
    (void)my_data;
    return 0;
}
