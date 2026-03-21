@interface NSObject
+ (instancetype)alloc;
- (instancetype)init;
@end
@interface NSString : NSObject
@end
@interface NSArray : NSObject
+ (instancetype)arrayWithObjects:(const id [])objects count:(unsigned long)cnt;
@end
@interface NSDictionary : NSObject
+ (instancetype)dictionaryWithObjects:(const id [])objects forKeys:(const id [])keys count:(unsigned long)cnt;
@end
void _check(void) {
    id _v = @{
    @"users": @[@{@"name": @"Bob", @"tags": @[@"admin", @"user"]}, @{@"name": @"Carol", @"tags": @[@"guest"]}],
};
    (void)_v;
}
