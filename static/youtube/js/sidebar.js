document.addEventListener("DOMContentLoaded", function(event) {
   
    const showNavbar = (toggleId, navId, bodyId, headerId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId),
    bodypd = document.getElementById(bodyId),
    headerpd = document.getElementById(headerId)

    search_bar=document.getElementById(search_form)
    
    
    // Validate that all variables exist
    if(toggle && nav && bodypd && headerpd){
    toggle.addEventListener('click', ()=>{
    // show navbar
    nav.classList.toggle('show')
    // change icon
    toggle.classList.toggle('bx-x')
    // add padding to body
    bodypd.classList.toggle('body-pd')
    // add padding to header
    headerpd.classList.toggle('body-pd')
    // Show Search Bar
    console.log(' class')
    if($('#search_form').hasClass('hide_search_bar')){
        console.log('add class')
        $('#search_form').removeClass('hide_search_bar')
        $('#search_form').addClass('show_search_bar')
    }
    else{
        $('#search_form').addClass('hide_search_bar')
        $('#search_form').removeClass('show_search_bar')
    }
    })
    }
    }
    
    showNavbar('header-toggle','nav-bar','body-pd','header')
    showNavbar('search_button','nav-bar','body-pd','header')
    
    /*===== LINK ACTIVE =====*/
    const linkColor = document.querySelectorAll('.nav_link')
    
    function colorLink(){
    if(linkColor){
    linkColor.forEach(l=> l.classList.remove('active'))
    this.classList.add('active')
    }
    }
    linkColor.forEach(l=> l.addEventListener('click', colorLink))
    
     // Your code to run since DOM is loaded and ready
    });