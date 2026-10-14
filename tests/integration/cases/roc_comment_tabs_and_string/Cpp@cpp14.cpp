#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, std::string>{
    // before	line
    {"value", "left\tright"},  // inline	line
    // after	line
};
    (void)my_data;
    return 0;
}
