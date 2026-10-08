Imports System.Collections.Generic
Module Check
    Function f(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim ref_data = New Integer()() {
            New Integer() {
                1,
                2
            },
            New Integer() {
                3,
                4
            }
        }
        f(New Integer()()()() {
            New Integer()()() {
                ref_data
            }
        })
    End Sub
End Module
