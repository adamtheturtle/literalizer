#include <cjson/cJSON.h>
static void process(cJSON *_a0) { (void)_a0; }
int main(void) {
process(cJSON_CreateString("hello"));
process(cJSON_CreateNumber((double)42));
process(cJSON_CreateBool(1));
    return 0;
}
