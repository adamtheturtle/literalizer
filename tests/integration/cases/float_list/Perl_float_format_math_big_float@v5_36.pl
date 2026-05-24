use Math::BigFloat;
{
    package LiteralizerFloat;
    our @ISA = ('Math::BigFloat');
    sub new { my ($c, $s) = @_; bless { _s => $s }, $c }
    sub bstr { $_[0]->{_s} }
}
my $my_data = [
    LiteralizerFloat->new("1.1"),
    LiteralizerFloat->new("-2.2"),
    LiteralizerFloat->new("3.3"),
];
