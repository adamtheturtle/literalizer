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
    @"date": @"2024-01-15",
    @"datetime": @"2024-01-15T12:30:00+00:00",
};
    (void)_v;
}
