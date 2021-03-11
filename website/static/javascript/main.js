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
        file_label.style.display = "inline-block";

        button.innerHTML = "Use URL";
    }

    // for some reason you have to press the button twice, but i do not
    // know why

}

