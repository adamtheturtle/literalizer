#include <initializer_list>
#include <string>
#include <map>
struct Record0 { std::string host; int port{}; bool debug{}; };
int main() {
auto my_data = Record0{
    // Server configuration
    "localhost",  // default host
    8080,
    // Enable debug mode
    true,
};
    (void)my_data;
    return 0;
}
