#include <initializer_list>
#include <string>
#include <vector>
struct Record0 { std::string value; };
auto consume(auto...) { return 0; }
int main() {
auto item = Record0{
    .value = "owned",
};
consume(std::move(item));
    return 0;
}
