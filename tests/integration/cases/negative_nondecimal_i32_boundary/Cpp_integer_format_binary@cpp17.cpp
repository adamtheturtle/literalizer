#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, long long>{
    {"minimum", (-0b1111111111111111111111111111111 - 1)},
    {"below", -0b10110010110100000101111000000000LL},
};
    (void)my_data;
    return 0;
}
