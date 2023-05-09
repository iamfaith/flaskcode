var words = ["2030033050", "2130001055", "2230024146", "2230026001", "2230026004", "2230026006", "2230026007", "2230026016", "2230026019", "2230026022", "2230026036", "2230026044", "2230026046", "2230026055", "2230026058", "2230026063", "2230026067", "2230026072", "2230026076", "2230026079", "2230026085", "2230026086", "2230026094", "2230026096", "2230026100", "2230026102", "2230026107", "2230026108", "2230026114", "2230026120", "2230026122", "2230026123", "2230026126", "2230026134", "2230026139", "2230026141", "2230026145", "2230026152", "2230026158", "2230026160", "2230026165", "2230026167", "2230026169", "2230026180", "2230026182", "2230026187", "2230026188", "2230026196", "2230026202", "2230026206", "2230026208", "2230026209", "2230026213", "2230026217", "2230026218", "2230026223", "2230026228", "2230026230", "2230026237", "2230026240", "1930026058", "2030004041", "2030032030", "2130004019", "2130005010", "2130013006", "2130013031", "2130016066", "2130024051", "2130024291", "2130026007", "2130026158", "2230026002", "2230026008", "2230026013", "2230026014", "2230026021", "2230026028", "2230026031", "2230026038", "2230026041", "2230026042", "2230026045", "2230026047", "2230026048", "2230026049", "2230026050", "2230026053", "2230026061", "2230026065", "2230026068", "2230026081", "2230026091", "2230026093", "2230026095", "2230026098", "2230026099", "2230026105", "2230026118", "2230026121", "2230026127", "2230026128", "2230026130", "2230026133", "2230026135", "2230026140", "2230026143", "2230026144", "2230026147", "2230026149", "2230026150", "2230026151", "2230026162", "2230026163", "2230026164", "2230026166", "2230026173", "2230026177", "2230026190", "2230026192", "2230026193", "2230026203", "2230026211", "2230026214", "2230026215", "2230026225", "2230026232", "2030026231",
];
// Get the input element
// var input = document.querySelector("input");

// Create a div element to hold the suggestions
var suggestions = document.createElement("div");
suggestions.id = "suggestions";
suggestions.style.position = "absolute";
suggestions.style.display = "none";
suggestions.style.border = "1px solid black";
suggestions.style.backgroundColor = "white";
suggestions.style.zIndex = "9999";

// Append the suggestions div to the body
document.body.appendChild(suggestions);

// Listen for input events on the input element
document.addEventListener("input", function (event) {
    // Get the input value
    var target = event.target;
    var value = target.value;
    var input = target

    // debugger
    // Clear the suggestions div
    suggestions.innerHTML = "";

    // Hide the suggestions div if the input is empty
    if (value === "") {
        suggestions.style.display = "none";
        return;
    }

    // Show the suggestions div
    suggestions.style.display = "block";

    ///Get the position and size of the input element
    var rect = input.getBoundingClientRect();

    ///Set the position and size of the suggestions div
    suggestions.style.left = rect.left + "px";
    suggestions.style.top = rect.bottom + "px";
    suggestions.style.width = rect.width + "px";

    suggestions.style.left = input.offsetLeft + "px";
    suggestions.style.top = (input.offsetTop + rect.height) + "px";

    var currentFocus = 0;
    input.addEventListener("keydown", function (e) {
        // 获取列表中的所有列表项元素
        // var items = suggestionList.getElementsByTagName("li");
        // 如果用户按下向下箭头键
        // e.stopPropagation()
        // console.log(e.keyCode)

        var items = document.getElementsByClassName("suggest-items");

        if (!event.repeat) {
            if (e.keyCode == 40) {

                items[currentFocus].style.background = '';

                currentFocus++;
                currentFocus = currentFocus % items.length;
                // console.log("keydown"); // down 
                items[currentFocus].style.background = "bisque";

            } else if (e.keyCode == 38) {
                items[currentFocus].style.background = '';
                // up
                currentFocus--;
                currentFocus = currentFocus % items.length;
                items[currentFocus].style.background = "bisque";
            } else if (e.keyCode == 13) {
                // enter
                if (currentFocus >= 0)
                    input.value = items[currentFocus].textContent;
                // Hide the suggestions div
                suggestions.style.display = "none";
            } else if (e.keyCode == 37 || e.keyCode == 39) {
                currentFocus = -1;
                suggestions.style.display = "none";
            }
        }
    });

    // Get the data array or create a new one if it doesn't exist
    var data = words;

    // Filter the data array by matching the input value
    var filteredData = data.filter(function (item) {
        // return item.startsWith(value);
        return item.includes(value);
    });

    // Sort the filtered data by length
    filteredData.sort(function (a, b) {
        return a.length - b.length;
    });

    // Limit the number of suggestions to 10
    filteredData = filteredData.slice(0, 10);

    // Loop through the filtered data and create a suggestion element for each item
    for (var i = 0; i < filteredData.length; i++) {
        var item = filteredData[i];

        // Create a span element to hold the suggestion text
        var span = document.createElement("span");
        span.textContent = item;



        // Create a div element to wrap the span element
        var div = document.createElement("div");
        div.appendChild(span);

        // Add some styles to the div element
        div.style.padding = "5px";
        div.style.cursor = "pointer";
        if (i == 0)
            div.style.background = "bisque";
        div.className = "suggest-items"

        // Add a click event listener to the div element
        div.addEventListener("click", function () {
            // Set the input value to the suggestion text
            input.value = this.textContent;

            // Hide the suggestions div
            suggestions.style.display = "none";
        });



        // Append the div element to the suggestions div
        suggestions.appendChild(div);
    }
});


var sid = document.getElementById("sid");

// Add an event listener for the keypress event
sid.addEventListener("keypress", function (event) {
    // Check if the key pressed was enter (key code 13)
    if (event.key === "Enter") {
        // Call the function
        // Get the current URL
        var currentURL = window.location.href;
        parts = currentURL.split('/')
        // var newURL = currentURL.replace(parts[parts.length], sid.value)
        // window.location.href = newURL
        // window.location.replace(newURL);
        
        window.history.replaceState("data", "title", "/" + parts[parts.length - 2] + "/" + sid.value);
        window.location.reload();
        
        // Print it to the console
        // console.log(currentURL);
    }
});