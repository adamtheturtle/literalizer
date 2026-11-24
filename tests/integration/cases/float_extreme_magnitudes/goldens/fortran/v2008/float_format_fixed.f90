module fval_m
  use, intrinsic :: iso_fortran_env, only: int64, real64
  implicit none
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
        freal(0.00000000000000000000000000000000000000000000000000000000000000&
    &0000000000000000000000000000000000000000000000000000000000000000&
    &0000000000000000000000000000000000000000000000000000000000000000&
    &0000000000000000000000000000000000000000000000000000000000000000&
    &0000000000000000000000000000000000000000000000000000000000000000&
    &000005_real64), &
        freal(0.00000000000000000000000000000000000000000000000000000000000000&
    &0000000000000000000000000000000000000000000000000000000000000000&
    &0000000000000000000000000000000000000000000000000000000000000000&
    &0000000000000000000000000000000000000000000000000000000000000000&
    &0000000000000000000000000000000000000000000000000000022250738585&
    &072014_real64), &
        freal(0.00000000000000000000000000000000000000000000000000000000000000&
    &0000000000000000000000000000000000000000000000000000000000000000&
    &0000000000000000000000000000000000000000000000000000000000000000&
    &0000000000000000000000000000000000000000000000000000000000000000&
    &00000000000000000000000000000000000000000000000000001_real64), &
        freal(1000000000000000000000.000000_real64), &
        freal(-150000000000000007875714038280663037305670287166223873237378117&
    &3267703686983362293679557062620671796065556665749325817265413784&
    &8530406458634671882771800604742725808013898637056067453506921821&
    &3508905342985245619991762167855845146132011197911417021374186888&
    &8183230085264257173504208294580298189100810240.000000_real64), &
        freal(1797693134862315708145274237317043567980705675258449965989174768&
    &0315726078002853876058955863276687817154045895351438246423432132&
    &6889464182768467546703537516986049910576551282076245490090389328&
    &9440758685084551339423045832369032229481658085593321233482747978&
    &26204144723168738177180919299881250404026184124858368.000000_rea&
    &l64), &
        freal(-179769313486231570814527423731704356798070567525844996598917476&
    &8031572607800285387605895586327668781715404589535143824642343213&
    &2688946418276846754670353751698604991057655128207624549009038932&
    &8944075868508455133942304583236903222948165808559332123348274797&
    &826204144723168738177180919299881250404026184124858368.000000_re&
    &al64) &
    ])
end program main
