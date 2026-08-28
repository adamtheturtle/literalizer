#include <initializer_list>
#include <string>
#include <vector>
#include <utility>
#include <variant>
struct Record1 { std::vector<int> numbers; std::vector<std::string> strings; };
struct Record0 { std::vector<std::pair<std::string, int>> omap_value; Record1 sibling_lists; std::vector<std::string> ref_marker_present; };
int main() {
auto my_data = Record0{
    .omap_value = {
        {"first", 1},
    },
    .sibling_lists = {
        .numbers = {
            1,
            2,
        },
        .strings = {
            "x",
            "y",
        },
    },
    .ref_marker_present = {
        "$keep",
        "z",
    },
};
    (void)my_data;
    return 0;
}
