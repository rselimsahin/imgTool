var count=0;
/*
var container1=document.getElementById("test-info")
var btn=document.getElementById("test");

btn.addEventListener("click", function() {
    var request=new XMLHttpRequest();
    request.open('GET','https://learnwebcode.github.io/json-example/animals-1.json')
    request.onload=function(){
        console.log("dadad")
        if(request.status>=200 && request.status<=400){
            var data=JSON.parse(request.responseText);
            renderHtml(data,container1);
        };
    };
    request.send();
});
*/
var container2=document.getElementById("div_addRule")
var btn2=document.getElementById("btn_addRule");

btn2.addEventListener("click", function() {
    console.log("xxx")
    var request=new XMLHttpRequest();
    request.open('GET','http://localhost:8000/client/addRule/')
    request.onload=function(){
        console.log(request.responseText)
        if(request.status>=200 && request.status<=400){
            var data=JSON.parse(request.responseText);
            renderHtml(data,container2);
        };
    };
    request.send();
});




function renderHtml(data, container){
    var html="";
    for(i=0;i<data.length;i++){
        html+="<p>"+data[i]+"</p>";
    }
    container.insertAdjacentHTML('beforeend',html);
}