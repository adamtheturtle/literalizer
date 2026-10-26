#include <map>
#include <string>
int main() {
auto my_data = std::map<std::string, long long>{
    {"lower", 3735928559},
    {"upper", 31},
    {"negative", -16},
    {"zero", 0},
};
    (void)my_data;
    return 0;
}
