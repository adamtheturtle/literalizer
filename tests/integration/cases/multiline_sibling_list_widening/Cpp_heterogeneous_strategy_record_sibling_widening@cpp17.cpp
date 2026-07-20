#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <utility>
#include <variant>
struct Record1 { std::vector<int> numbers; std::vector<std::string> strings; };
struct Record0 { std::vector<std::pair<std::string, int>> omap_value; Record1 sibling_lists; std::vector<std::string> ref_marker_present; };
int main() {
auto my_data = Record0{
    .omap_value = std::vector<std::pair<std::string, int>>{
        {"first", 1},
    },
    .sibling_lists = Record1{
        .numbers = std::vector<int>{
            1,
            2,
        },
        .strings = std::vector<std::string>{
            "x",
            "y",
        },
    },
    .ref_marker_present = std::vector<std::string>{
        "$keep",
        "z",
    },
};
    (void)my_data;
    return 0;
}
