typedef signed char BOOL;
#define YES ((BOOL)1)
#define NO ((BOOL)0)
@interface NSObject
+ (instancetype)alloc;
- (instancetype)init;
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
@interface NSArray : NSObject
+ (instancetype)arrayWithObjects:(const id [])objects count:(unsigned long)cnt;
@end
void _check(void) {
id my_data = @[
    @(1),
    @(2),
    @(3),
];
    (void)my_data;
}
