#include <initializer_list>
#include <string>
#include <vector>
struct Record0 { int value{}; };
auto consume(auto...) { return 0; }
int main() {
auto item = Record0{
    .value = 1,
};
consume(item);
    return 0;
}
