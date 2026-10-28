#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::variant<long, std::vector<long>>>{
    -2147483648L,
    -2147483647L,
    std::vector<long>{0L},
};
    (void)my_data;
    return 0;
}
