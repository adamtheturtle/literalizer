#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateArray();
cJSON *_n1 = cJSON_CreateString("C:\\path\\to\\file");
cJSON_AddItemToArray(_n0, _n1);
cJSON *_n2 = cJSON_CreateString("back\\\\slash");
cJSON_AddItemToArray(_n0, _n2);
cJSON *_n3 = cJSON_CreateString("hello \\\"world\\\"");
cJSON_AddItemToArray(_n0, _n3);
cJSON *_n4 = cJSON_CreateString("path\\to \"# file");
cJSON_AddItemToArray(_n0, _n4);
cJSON *_n5 = cJSON_CreateString("trailing\\");
cJSON_AddItemToArray(_n0, _n5);
cJSON *_n6 = cJSON_CreateString("both \"quotes''' here");
cJSON_AddItemToArray(_n0, _n6);
cJSON *_n7 = cJSON_CreateString("line1\\nline2\nwith newline");
cJSON_AddItemToArray(_n0, _n7);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
