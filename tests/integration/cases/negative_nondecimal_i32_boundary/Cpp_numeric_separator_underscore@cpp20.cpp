#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long long>{
    {"minimum", (-2'147'483'647 - 1)},
    {"below", -3'000'000'000},
};
    (void)my_data;
    return 0;
}
