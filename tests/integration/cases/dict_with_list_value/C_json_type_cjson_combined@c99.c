#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateString("Alice");
cJSON_AddItemToObject(_n0, "name", _n1);
cJSON *_n2 = cJSON_CreateArray();
cJSON *_n3 = cJSON_CreateNumber((double)10);
cJSON_AddItemToArray(_n2, _n3);
cJSON *_n4 = cJSON_CreateNumber((double)20);
cJSON_AddItemToArray(_n2, _n4);
cJSON *_n5 = cJSON_CreateNumber((double)30);
cJSON_AddItemToArray(_n2, _n5);
cJSON_AddItemToObject(_n0, "scores", _n2);
cJSON *my_data = _n0;
(void)my_data;
cJSON *_m6 = cJSON_CreateObject();
cJSON *_m7 = cJSON_CreateString("Alice");
cJSON_AddItemToObject(_m6, "name", _m7);
cJSON *_m8 = cJSON_CreateArray();
cJSON *_m9 = cJSON_CreateNumber((double)10);
cJSON_AddItemToArray(_m8, _m9);
cJSON *_m10 = cJSON_CreateNumber((double)20);
cJSON_AddItemToArray(_m8, _m10);
cJSON *_m11 = cJSON_CreateNumber((double)30);
cJSON_AddItemToArray(_m8, _m11);
cJSON_AddItemToObject(_m6, "scores", _m8);
my_data = _m6;
    (void)my_data;
    return 0;
}
