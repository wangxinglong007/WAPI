function display(d) {
    var ui = document.getElementById(d);
    if(ui.style.display=="block"){
        ui.style.display="none";
    }
    else{
        ui.style.display="block";
    }
}
window.alert = alert;
function alert(data) {
    var pup = document.createElement("div"),
    section = document.createElement("section")
    error_message = document.createElement("p"),
    btn = document.createElement("div"),
    error_title = document.createElement("div"),
    textNode = document.createTextNode(data ? data : ""),
    error_title_measage = document.createTextNode("");
    btnText = document.createTextNode("Close");
    // 控制样式
    css(pup, {
        "position" : "absolute",
        "left" : "20%",
        "right" : "20%",
        "top" : "10%",
        "bottom" : "30%",
        "margin" : "50px",
        "background-color" : "#FFFCEC",
        "text-align" : "left",
        //"width" : "auto",
        "overflow-x" : "auto",
        "overflow-y" : "auto"
    });
    css(error_message, {
        "font-size" : "15px",
    })
    css(btn, {
        "background" : "#999999",
        "text-align" : "right",
        "color" : "white",
    })
    // 内部结构套入
    btn.appendChild(btnText);
    pup.appendChild(btn);

    error_title.appendChild(error_title_measage);
    pup.appendChild(error_title);

    error_message.appendChild(textNode);

    pup.appendChild(section);
    section.appendChild(error_message);


    // 整体显示到页面内
    document.getElementsByTagName("body")[0].appendChild(pup);
    // 点击关闭按钮
    btn.onclick = function() {
        pup.parentNode.removeChild(pup);
    }
}
function css(targetObj, cssObj) {
    var str = targetObj.getAttribute("style") ? targetObj.getAttribute("style") : "";
    for(var i in cssObj) {
        str += i + ":" + cssObj[i] + ";";
    }
    targetObj.style.cssText = str;
}
//alert(ui.innerHTML);

function display(d) {
    var ui = document.getElementById(d);
    alert(ui.innerHTML);
    //如果以弹框的形式，那这个就不显示
    /*if (ui.style.display == "block") {
        ui.style.display = "none";
    } else {
        ui.style.display = "block";
    }*/
}
