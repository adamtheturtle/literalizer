#include <cjson/cJSON.h>
int main(void) {
cJSON *_n5 = cJSON_CreateNumber((double)42);
cJSON *shared = _n5;
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateArray();
cJSON *_n2 = cJSON_Duplicate(shared, 1);
cJSON_AddItemToArray(_n1, _n2);
cJSON *_n3 = cJSON_Duplicate(shared, 1);
cJSON_AddItemToArray(_n1, _n3);
cJSON_AddItemToObject(_n0, "refs", _n1);
cJSON *_n4 = cJSON_CreateString("#{shared}");
cJSON_AddItemToObject(_n0, "quoted", _n4);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
