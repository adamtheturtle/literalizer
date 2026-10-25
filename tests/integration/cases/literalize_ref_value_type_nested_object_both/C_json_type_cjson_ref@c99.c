#include <cjson/cJSON.h>
int main(void) {
cJSON *_n4 = cJSON_CreateArray();
cJSON *_n5 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(_n4, _n5);
cJSON *_n6 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(_n4, _n6);
cJSON *shared = _n4;
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_Duplicate(shared, 1);
cJSON_AddItemToObject(_n0, "field", _n1);
cJSON *my_data = _n0;
(void)my_data;
cJSON *_m2 = cJSON_CreateObject();
cJSON *_m3 = cJSON_Duplicate(shared, 1);
cJSON_AddItemToObject(_m2, "field", _m3);
my_data = _m2;
    (void)my_data;
    return 0;
}
