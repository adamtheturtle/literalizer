Imports System.Collections.Generic
Module Check
    Function make_widget(items As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        Dim my_data = make_widget(New Integer()() {New Integer() {1, 2}, New Integer() {3}})
    End Sub
End Module
