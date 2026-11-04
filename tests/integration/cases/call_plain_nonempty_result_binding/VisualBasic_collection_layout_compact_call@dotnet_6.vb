Imports System.Collections.Generic
Module Check
    Function make_widget(value As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_data = make_widget(New Integer() {1})
    End Sub
End Module
