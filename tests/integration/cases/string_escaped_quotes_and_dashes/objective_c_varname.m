@interface NSObject
+ (instancetype)alloc;
- (instancetype)init;
@end
@interface NSString : NSObject
@end
void _check(void) {
id my_data = @"hello \"world\" -- not a comment";
    (void)my_data;
}
