// const inputOfUser = $("#user_input")
// const search_icon = $('#search-icon')
// const artists_div = $('#replaceable-content')
//  // jQuery selector to save those elements as variables so we can more easily refer to them later in the code
// const endpoint = ''
// const delay_by_in_ms = 300
// let scheduled_function = false
//
// console.log('Im in main')
//
// let ajax_call = function (endpoint, request_parameters) {
//       console.log('Im in the function')
//       $.getJSON(endpoint, request_parameters)
//         .done(response => {
//             // fade out the artists_div, then:
//             artists_div.fadeTo('slow', 0).promise().then(() => {
//                 // replace the HTML contents
//                 artists_div.html(response['html_from_view'])
//                 // fade-in the div with new contents
//                 artists_div.fadeTo('slow', 1)
//                 // stop animating search icon
//                 search_icon.removeClass('blink')
//             })
//         })
// }
//
// // This means that each time a keyboard key is released (after being pressed) inside user_input, the function is run
// inputOfUser.on('keyup', function () {
//     console.log('Im in the user input value')
//     console.log($(this).val())
//     const request_parameters = {
//         q: $(this).val() // value of user_input: the HTML element with ID user-input
//     }
//
//     // start animating the search icon with the CSS class
//     search_icon.addClass('blink')
//
//     // if scheduled_function is NOT false, cancel the execution of the function
//     if (scheduled_function) {
//         clearTimeout(scheduled_function)
//     }
//
//     // setTimeout returns the ID of the function to be executed
//     scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
// })
