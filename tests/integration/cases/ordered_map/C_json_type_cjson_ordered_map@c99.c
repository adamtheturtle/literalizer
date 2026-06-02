#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateString("Alice");
cJSON_AddItemToObject(_n0, "name", _n1);
cJSON *_n2 = cJSON_CreateNumber((double)30);
cJSON_AddItemToObject(_n0, "age", _n2);
cJSON *_n3 = cJSON_CreateBool(1);
cJSON_AddItemToObject(_n0, "active", _n3);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
