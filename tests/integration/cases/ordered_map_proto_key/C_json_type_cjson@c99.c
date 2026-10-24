#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateObject();
cJSON *_n2 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(_n1, "x", _n2);
cJSON_AddItemToObject(_n0, "__proto__", _n1);
cJSON *_n3 = cJSON_CreateNumber((double)2);
cJSON_AddItemToObject(_n0, "ordinary", _n3);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
