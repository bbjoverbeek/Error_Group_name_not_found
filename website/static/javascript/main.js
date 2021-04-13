function switchScriptUrlFile() {
    var url_input = document.getElementById("url_script");
    var file_input = document.getElementById("script")
    var file_label = document.getElementById("label_script_file");
    var button = document.getElementById("url_or_script");

    if (file_input.style.display === "block") {

        url_input.style.display = "block";

        file_label.style.display = "none";
        file_input.style.display = "none";

        button.innerHTML = "Use file";

    } else {
        url_input.style.display = "none";

        file_input.style.display = "block";
        file_label.style.display = "block";

        button.innerHTML = "Use URL";
    }
}


function show_continue_process() {
    var continue_process_div = document.getElementById("continue_process")
    
    if (continue_process_div.classList.contains("active")) {
        continue_process_div.classList.replace("active", "not_active");
    } else {
        continue_process_div.classList.replace("not_active", "active")
    }
}




// $(document).ready(function() {
//     $('form#upload_files').on('submit', function(event) {
// 
//         event.preventDefault();
// 
// 
//         var upload_files = new FormData($("form")[0, 1, 2, 3, 4]);
//         
// 
//         $.ajax({
//             data : upload_files,
//             dataType : false,
//             enctype: 'multipart/form-data',
//             type : "POST",
//             url : "/"
//         })
// 
//        
//     }); 
// });

    










// $(window).load(function() {
//     // Animate loader off screen
//     $("#waiting_screen").toggle("scale");
// });




// function display_waiting() {
//     var waitingScreen = document.getElementById("waiting_screen")
//     console.log("it worked")
//     waitingScreen.style.scale = "1.0"
// }




// var interval = setInterval(update_progress, 1000);
// function update_progress() {
//      $.get('/progress').done(function(n){
//          n = n / 5;  // percent value
//          if (n == 100) {
//             clearInterval(interval);
//             callback(); // user defined
//          }
//          $('#progress-bar').animate({'width': n +'%'}).attr// ('aria-valuenow', n);
//          console.log(n)    
//      }).fail(function() {
//          clearInterval(interval);
//          displayerror(); // user defined
//      });
// }








// var interval = setInterval(update_progress, 1000);
// function update_progress() {
//     request = $.ajax({
//         url : "/progress",
//         type : "GET",
//         success: function(data){
//             console.log(data);
//             document.getElementById('progress_bar').innerHTML = data; 
//         }
//     });
// 
// 
// 
//     // $.get('/progress').done(function(n){
//     //     n = n / 5;  // percent value
//     //     if (n == 100) {
//     //        clearInterval(interval);
//     //        callback(); // user defined
//     //     }
//     //     $('#progress').innerHTML = n;    
//     // }).fail(function() {
//     //     clearInterval(interval);
//     //     displayerror(); // user defined
//     // });
// }