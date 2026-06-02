#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateArray();
cJSON *_n1 = cJSON_CreateString("48656c6c6f");
cJSON_AddItemToArray(_n0, _n1);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
