#include <initializer_list>
#include <string>
#include <vector>
struct Record0 { std::string value; };
template <typename... Args> auto consume(Args...) { return 0; }
int main() {
auto item = Record0{
    "owned",
};
consume(std::move(item));
    return 0;
}
