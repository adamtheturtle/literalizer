#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateString("_");
cJSON_AddItemToObject(_n0, "_", _n1);
cJSON *userObj = _n0;
cJSON * my_data = userObj;
    (void)my_data;
    return 0;
}
