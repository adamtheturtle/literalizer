typedef signed char BOOL;
#define YES ((BOOL)1)
#define NO ((BOOL)0)
@interface NSObject
+ (instancetype)alloc;
- (instancetype)init;
@end
@interface NSString : NSObject
@end
@interface NSNumber : NSObject
+ (instancetype)numberWithBool:(BOOL)value;
+ (instancetype)numberWithChar:(signed char)value;
+ (instancetype)numberWithInt:(int)value;
+ (instancetype)numberWithUnsignedInt:(unsigned int)value;
+ (instancetype)numberWithLong:(long)value;
+ (instancetype)numberWithUnsignedLong:(unsigned long)value;
+ (instancetype)numberWithLongLong:(long long)value;
+ (instancetype)numberWithUnsignedLongLong:(unsigned long long)value;
+ (instancetype)numberWithFloat:(float)value;
+ (instancetype)numberWithDouble:(double)value;
@end
@interface NSDictionary : NSObject
+ (instancetype)dictionaryWithObjects:(const id [])objects forKeys:(const id [])keys count:(unsigned long)cnt;
@end
void _check(void) {
    id _v = @{
    @"name": @"Alice",
    @"age": @(30),
    @"active": @YES,
};
    (void)_v;
}
