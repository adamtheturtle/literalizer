module fval_m
  implicit none
  integer, parameter :: int64 = selected_int_kind(18)
  integer, parameter :: real64 = selected_real_kind(15, 307)
  integer, parameter :: tag_null = 0
  integer, parameter :: tag_bool = 1
  integer, parameter :: tag_int = 2
  integer, parameter :: tag_real = 3
  integer, parameter :: tag_str = 4
  integer, parameter :: tag_list = 5
  integer, parameter :: tag_map = 6
  integer, parameter :: tag_set = 7
  integer, parameter :: tag_entry = 8
  type :: fval_t
    integer :: tag = tag_null
    logical :: bv = .false.
    integer(kind=int64) :: iv = 0_int64
    real(kind=real64) :: rv = 0.0_real64
    character(len=:), pointer :: sv => null()
    type(fval_t), pointer :: items(:) => null()
  end type fval_t
contains
  function fnull() result(v)
    type(fval_t) :: v
    v%tag = tag_null
  end function fnull
  function fbool(b) result(v)
    logical, intent(in) :: b
    type(fval_t) :: v
    v%tag = tag_bool
    v%bv = b
  end function fbool
  function fint(n) result(v)
    integer(kind=int64), intent(in) :: n
    type(fval_t) :: v
    v%tag = tag_int
    v%iv = n
  end function fint
  function freal(x) result(v)
    real(kind=real64), intent(in) :: x
    type(fval_t) :: v
    v%tag = tag_real
    v%rv = x
  end function freal
  function fstr(s) result(v)
    character(len=*), intent(in) :: s
    type(fval_t) :: v
    v%tag = tag_str
    allocate(character(len=len(s)) :: v%sv)
    v%sv = s
  end function fstr
  function flist(a) result(v)
    type(fval_t), intent(in) :: a(:)
    type(fval_t) :: v
    v%tag = tag_list
    allocate(v%items(size(a)))
    v%items = a
  end function flist
  function fmap(a) result(v)
    type(fval_t), intent(in) :: a(:)
    type(fval_t) :: v
    v%tag = tag_map
    allocate(v%items(size(a)))
    v%items = a
  end function fmap
  function fset(a) result(v)
    type(fval_t), intent(in) :: a(:)
    type(fval_t) :: v
    v%tag = tag_set
    allocate(v%items(size(a)))
    v%items = a
  end function fset
  function fentry(k, u) result(v)
    character(len=*), intent(in) :: k
    type(fval_t), intent(in) :: u
    type(fval_t) :: v
    v%tag = tag_entry
    allocate(character(len=len(k)) :: v%sv)
    v%sv = k
    allocate(v%items(1))
    v%items(1) = u
  end function fentry
end module fval_m
program main
    use fval_m
    implicit none
    type(fval_t) :: my_data
    my_data = flist([fval_t :: &
        fint(0_int64), &
        fint(1_int64), &
        fint(2_int64), &
        fint(3_int64), &
        fint(4_int64), &
        fint(5_int64), &
        fint(6_int64), &
        fint(7_int64), &
        fint(8_int64), &
        fint(9_int64), &
        fint(10_int64), &
        fint(11_int64), &
        fint(12_int64), &
        fint(13_int64), &
        fint(14_int64), &
        fint(15_int64), &
        fint(16_int64), &
        fint(17_int64), &
        fint(18_int64), &
        fint(19_int64), &
        fint(20_int64), &
        fint(21_int64), &
        fint(22_int64), &
        fint(23_int64), &
        fint(24_int64), &
        fint(25_int64), &
        fint(26_int64), &
        fint(27_int64), &
        fint(28_int64), &
        fint(29_int64), &
        fint(30_int64), &
        fint(31_int64), &
        fint(32_int64), &
        fint(33_int64), &
        fint(34_int64), &
        fint(35_int64), &
        fint(36_int64), &
        fint(37_int64), &
        fint(38_int64), &
        fint(39_int64), &
        fint(40_int64), &
        fint(41_int64), &
        fint(42_int64), &
        fint(43_int64), &
        fint(44_int64), &
        fint(45_int64), &
        fint(46_int64), &
        fint(47_int64), &
        fint(48_int64), &
        fint(49_int64), &
        fint(50_int64), &
        fint(51_int64), &
        fint(52_int64), &
        fint(53_int64), &
        fint(54_int64), &
        fint(55_int64), &
        fint(56_int64), &
        fint(57_int64), &
        fint(58_int64), &
        fint(59_int64), &
        fint(60_int64), &
        fint(61_int64), &
        fint(62_int64), &
        fint(63_int64), &
        fint(64_int64), &
        fint(65_int64), &
        fint(66_int64), &
        fint(67_int64), &
        fint(68_int64), &
        fint(69_int64), &
        fint(70_int64), &
        fint(71_int64), &
        fint(72_int64), &
        fint(73_int64), &
        fint(74_int64), &
        fint(75_int64), &
        fint(76_int64), &
        fint(77_int64), &
        fint(78_int64), &
        fint(79_int64), &
        fint(80_int64), &
        fint(81_int64), &
        fint(82_int64), &
        fint(83_int64), &
        fint(84_int64), &
        fint(85_int64), &
        fint(86_int64), &
        fint(87_int64), &
        fint(88_int64), &
        fint(89_int64), &
        fint(90_int64), &
        fint(91_int64), &
        fint(92_int64), &
        fint(93_int64), &
        fint(94_int64), &
        fint(95_int64), &
        fint(96_int64), &
        fint(97_int64), &
        fint(98_int64), &
        fint(99_int64), &
        fint(100_int64), &
        fint(101_int64), &
        fint(102_int64), &
        fint(103_int64), &
        fint(104_int64), &
        fint(105_int64), &
        fint(106_int64), &
        fint(107_int64), &
        fint(108_int64), &
        fint(109_int64), &
        fint(110_int64), &
        fint(111_int64), &
        fint(112_int64), &
        fint(113_int64), &
        fint(114_int64), &
        fint(115_int64), &
        fint(116_int64), &
        fint(117_int64), &
        fint(118_int64), &
        fint(119_int64) &
    ])
end program main
