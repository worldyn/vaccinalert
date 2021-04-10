(function () {

    var clockElement = document.getElementById( "clock" );



    var d = new Date();
    d.setMinutes(d.getMinutes() - 1);

    h = (d.getHours()<10?'0':'') + d.getHours(),
    m = (d.getMinutes()<10?'0':'') + d.getMinutes();



    clockElement.innerHTML  = h + ':' + m;



    

    function updateClock ( clock ) {

        //clock.innerHTML = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        var d = new Date();
        d.setMinutes(d.getMinutes() - 1);

        var h = (d.getHours()<10?'0':'') + d.getHours(),
        m = (d.getMinutes()<10?'0':'') + d.getMinutes();
        
        clock.innerHTML  = h + ':' + m;

    }


    setInterval(function () {
        updateClock( clockElement );
    }, 1000);
        
    
  }());