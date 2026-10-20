Imports System.Collections.Generic
Module Check
    Function make_widget(before As Object, populated As Object, after As Object) As Object
        Return Nothing
    End Function
    Sub _calls()
        make_widget(New Object() {}, New Integer() {1}, New Object() {})
        make_widget(New String() {"text"}, New Integer() {2}, New Object() {})
        make_widget(New Object() {}, New String() {"text"}, New Object() {})
        make_widget(New String() {"text"}, New Integer() {2}, New Integer() {3})
    End Sub
End Module
