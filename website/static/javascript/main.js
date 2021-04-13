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