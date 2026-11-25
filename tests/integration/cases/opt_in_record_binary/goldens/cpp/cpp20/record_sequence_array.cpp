#include <string>
struct Record0 { std::string payload; };
int main() {
auto my_data = Record0{
    .payload = "616263",
};
    (void)my_data;
    return 0;
}
