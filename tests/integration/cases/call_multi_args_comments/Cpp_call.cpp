#include <initializer_list>
#include <vector>
auto process(auto...) { return 0; }
int main() {
process(1, 0, 3600);  // Jan 1 1970 00:00:00 - 01:00:00
process(5, 0, 3600);  // Jan 1 1970 00:00:05 - 01:00:05
process(2, 0, 5400);  // Jan 1 1970 00:00:02 - 01:30:02
    return 0;
}
