#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long long>{
    {"minimum", -0b10000000000000000000000000000000LL},
    {"below", -0b10110010110100000101111000000000LL},
};
    (void)my_data;
    return 0;
}
