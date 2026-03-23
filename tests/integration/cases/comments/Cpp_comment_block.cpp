#include <initializer_list>
#include <string>
#include <map>
void _check() {
    [[maybe_unused]] _Any _v = {
    /* Server configuration */
    {"host", "localhost"},  /* default host */
    {"port", 8080},
    /* Enable debug mode */
    {"debug", true},
};
}
