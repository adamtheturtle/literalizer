Imports System.Collections.Generic
Module Check
    Function f(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim ref_data = New Integer() {
            1,
            2
        }
        f(New Integer()() {
            ref_data
        })
        f(New Integer()() {
            ref_data
        })
    End Sub
End Module
