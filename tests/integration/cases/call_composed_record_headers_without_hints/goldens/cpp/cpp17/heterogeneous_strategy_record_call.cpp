#include <string>
#include <vector>
struct Record0 { std::string name; std::vector<int> values; };
template <typename... Args> auto consume(Args...) { return 0; }
int main() {
auto item = Record0{
    "first",
    {
        1,
        2,
    },
};
consume(item);
    return 0;
}
