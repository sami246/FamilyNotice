// $(function(){
//    $.ajax({
//             url: "{% url 'List of lists' %}",
//             success: function(data){
//               console.log(data)
//              for(var i=0;i<data.list.length; i++){
//                  var the_id = data.list[i].id
//                  $(".To_do_list").append("<li class='ToDoListRow' id=" + data.list[i].id + ">"
//                     + "<a href='/tasks/" + the_id + "'>" + data.list[i].nameOfList + "</a><br>"
//                     + "<button class='DeleteButton' id=" + data.list[i].id + "> Delete </button></li>")
//              }
//
//              $(".DeleteButton").click(function(){
//                  var deleteConf = confirm("Are you sure you want to delete this List permanently?");
//                  if (deleteConf == true){
//                       console.log($(this).attr("id"))
//                       csrfToken = $('input[name=csrfmiddlewaretoken]').val()
//                             $.ajax({
//                               url: "{% url 'delete list' %}",
//                               type : "DELETE",
//                               dataType: 'json',
//                               data: $(this).attr('id'),
//                               beforeSend: function (xhr) {
//                                      xhr.setRequestHeader("X-CSRFToken", '{{ csrf_token}}');
//                               },
//                               success: function(data){
//                                      console.log(data)
//                                      $('#'+data.values+'').remove()
//                                      console.log('memeber is deleted')
//                                      alert("The employee is deleted!");
//                               }
//                       })
//                   }
//               })
//               //END DELETE
//             }
//    })
//  })
