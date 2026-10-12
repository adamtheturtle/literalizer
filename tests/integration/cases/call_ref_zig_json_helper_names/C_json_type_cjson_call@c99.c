#include <cjson/cJSON.h>
static void process(cJSON *_a0) { (void)_a0; }
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(_n0, "a", _n1);
cJSON *arena = _n0;
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(_n0, "a", _n1);
cJSON *ZVal = _n0;
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(_n0, "a", _n1);
cJSON *ZKV = _n0;
process(arena);
process(ZVal);
process(ZKV);
    return 0;
}
