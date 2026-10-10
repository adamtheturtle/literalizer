#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long long>{
    {"minimum", -0x80000000LL},
    {"below", -0xb2d05e00LL},
};
    (void)my_data;
    return 0;
}
