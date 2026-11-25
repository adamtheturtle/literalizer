#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, long long>{
    {"minimum", (-0x7fffffff - 1)},
    {"below", -0xb2d05e00LL},
};
    (void)my_data;
    return 0;
}
