@interface NSObject
+ (instancetype)alloc;
- (instancetype)init;
@end
@interface NSString : NSObject
@end
@interface NSDictionary : NSObject
+ (instancetype)dictionaryWithObjects:(const id [])objects forKeys:(const id [])keys count:(unsigned long)cnt;
@end
void _check(void) {
    id _v = @{
    @"key\nwith\nnewlines": @"value1",
    @"key\twith\ttabs": @"value2",
    @"": @"value3",
};
    (void)_v;
}
