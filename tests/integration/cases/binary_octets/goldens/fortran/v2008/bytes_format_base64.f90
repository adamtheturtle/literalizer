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
        fstr(''), &
        fstr('AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0x' // &
    & 'NTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZ' // &
    & 'qbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5' // &
    & '+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/w=='), &
        fstr('//79/Pv6+fj39vX08/Lx8O/u7ezr6uno5+bl5OPi4eDf3t3c29rZ2NfW1dTT0tHQz87NzMvKycjHxsXEw8LBwL++vby7urm4t7a1tLO' // &
    & 'ysbCvrq2sq6qpqKempaSjoqGgn56dnJuamZiXlpWUk5KRkI+OjYyLiomIh4aFhIOCgYB/fn18e3p5eHd2dXRzcnFwb25tbGtqaWhnZm' // &
    & 'VkY2JhYF9eXVxbWllYV1ZVVFNSUVBPTk1MS0pJSEdGRURDQkFAPz49PDs6OTg3NjU0MzIxMC8uLSwrKikoJyYlJCMiISAfHh0cGxoZG' // &
    & 'BcWFRQTEhEQDw4NDAsKCQgHBgUEAwIBAA==') &
    ])
end program main
