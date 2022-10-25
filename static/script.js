makeDecision = (user, comp) => {
    let win

    if (user == "r" && comp == "s") {
        win = true
    } else if (user == "s" && comp == "p")  {
        win = true
    } else if (user == "p" && comp == "r")  {
        win = true
    } else {
        win = false
    }

    let formattedComp
    if (comp == "s") {formattedComp = "scissors"}
    if (comp == "r") {formattedComp = "rock"}
    if (comp == "p") {formattedComp = "paper"}

    document.getElementById("body").innerHTML = "<p>Computer's choice: " + formattedComp + "<form method='post'><input type='hidden' value='" + String(win) + "' name='win'><button type='submit' class='btn'>Submit result</button></form>"
}