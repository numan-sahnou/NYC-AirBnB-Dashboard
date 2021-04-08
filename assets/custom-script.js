setTimeout(() => {
    document.getElementById('slct_web_mode').children[0].children[0].onclick= function(){
    document.getElementById('global').style.cssText='background-color:#202020; color:#21a1bb;'; //here we insert function onclick to the button wich choose the layoute of the graph
    console.log('dark-mode');                                                                   // in order tp change by the way the background color
    
}

    
    document.getElementById('slct_web_mode').children[1].children[0].onclick= function(){
    document.getElementById('global').style.cssText='background-color:#f8f8f0; color:#041417;';
    console.log('light-mode');
}

    document.getElementById('global').style.cssText='background-color:#f8f8f0; color:#041417;';
    document.getElementById('slct_room_type').children[0].children[0].children[0].children[0].children[1].style.cssText='color:black;'; // here we change the color of the choice in the seelct room type
    document.getElementById('slct_room_type').children[0].children[0].children[0].children[1].children[1].style.cssText='color:black;';
    document.getElementById('slct_room_type').children[0].children[0].children[0].children[2].children[1].style.cssText='color:black;';
    console.log(document.getElementById('slct_room_type').children[0].children[0].children[0].children[0]);

    console.log("c'est bon");
    
    }, 10000);