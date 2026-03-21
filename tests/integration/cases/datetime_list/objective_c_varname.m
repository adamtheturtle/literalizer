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
@interface NSArray : NSObject
+ (instancetype)arrayWithObjects:(const id [])objects count:(unsigned long)cnt;
@end
@interface NSDictionary : NSObject
+ (instancetype)dictionaryWithObjects:(const id [])objects forKeys:(const id [])keys count:(unsigned long)cnt;
@end
@interface NSNull : NSObject
+ (instancetype)null;
@end
@interface NSSet : NSObject
+ (instancetype)set;
+ (instancetype)setWithArray:(NSArray *)array;
@end
void _check(void) {
id my_data = @[
    @"2024-01-15T12:30:00+00:00",
    @"2024-06-30T08:00:00+00:00",
    @"2024-12-25T18:45:00+00:00",
];
    (void)my_data;
}
