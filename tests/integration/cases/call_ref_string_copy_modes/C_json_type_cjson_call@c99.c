#include <cjson/cJSON.h>
static void consume(cJSON *_a0) { (void)_a0; }
int main(void) {
cJSON *_n0 = cJSON_CreateString("s");
cJSON *item = _n0;
consume(item);
    return 0;
}
