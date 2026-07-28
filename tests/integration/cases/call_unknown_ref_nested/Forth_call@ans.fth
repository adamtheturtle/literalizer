: process ;
: known_value true +bool ;
: unknown_value true +bool ;
known_value +arr unknown_value -arr process
