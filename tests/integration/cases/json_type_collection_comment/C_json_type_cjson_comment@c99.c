#include <cjson/cJSON.h>
int main(void) {
// About a.
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(_n0, "a", _n1);
cJSON *_n2 = cJSON_CreateNumber((double)2);
cJSON_AddItemToObject(_n0, "b", _n2);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
