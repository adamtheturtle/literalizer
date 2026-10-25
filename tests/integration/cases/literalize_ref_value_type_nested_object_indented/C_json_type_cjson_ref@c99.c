#include <cjson/cJSON.h>
int main(void) {
        cJSON *_n6 = cJSON_CreateArray();
cJSON *_n7 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(_n6, _n7);
cJSON *_n8 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(_n6, _n8);
cJSON *shared = _n6;
        cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateObject();
cJSON *_n2 = cJSON_CreateArray();
cJSON *_n3 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(_n2, _n3);
cJSON *_n4 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(_n2, _n4);
cJSON_AddItemToObject(_n1, "nested", _n2);
cJSON_AddItemToObject(_n0, "field", _n1);
cJSON *_n5 = cJSON_CreateString("first\n{ \" // }");
cJSON_AddItemToObject(_n0, "text", _n5);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
