var mydata = JSON.parse(tloader);
var nowpag = 0;
var name = sessionStorage.getItem("title")
var title = "";
var subtitle = "";

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function loadpg(input){
        
    if((Object.size(mydata.tloader[0]) < input) || input <= 0) { alert("마지막 페이지 입니다!"); return ; }

    title = mydata.tloader[0][name][0].title;
    subtitle = mydata.tloader[0][name][0][input][0];
    
    var viewer = document.getElementById("viewer");

    removeTags();

    for(var i = 1; i <= mydata.tloader[0][name][0][input][1]; i++){
        var aTag = document.createElement("img");
        aTag.setAttribute("src", title + "/" + subtitle + "/" + i + ".png");
        viewer.appendChild(aTag);
    }

    nowpag = input;

    document.getElementById("cotpg").innerText = "#" + nowpag + " - " + subtitle;
    
    scrollTo(0, 0);
}

function homPg() {
    removeTags()
    document.getElementById("cotpg").innerText = "#";
    sessionStorage.setItem("title", "이츠마인");
    console.log("홈페이지");
}

function removeTags(){
    var viewer = document.getElementById("viewer");

    while (viewer.firstChild) {
        viewer.removeChild(viewer.firstChild);
    }

}

$(window).on('scroll', function(){
    var s = $(window).scrollTop(),
        d = $(document).height(),
        c = $(window).height();
  
    var scrollPercent = (s / (d - c)) * 100;

    if(scrollPercent == 100) { loadpg(nowpag + 1) }
  })

window.onload = function () {
    
    if(nowpag == 0) { homPg();};

    document.getElementsByClassName("navbar")[0].addEventListener("mouseover", mouseOver);
    document.getElementsByClassName("navbar")[0].addEventListener("mouseout", mouseOut);
    document.getElementById("prvpg").addEventListener("click", prvPg);
    document.getElementById("nxtpg").addEventListener("click", nxtPg);

    function nxtPg() {
        loadpg(nowpag + 1);
    }

    function prvPg() {

        if((nowpag - 1) <= 0) { homPg(); return ;};

        loadpg(nowpag - 1);
    }

    function mouseOver() {
        $(".navbar").animate({
            opacity:1,
          });
    }

    function mouseOut() {
        $(".navbar").animate({
            opacity:0,
          });
    }

}