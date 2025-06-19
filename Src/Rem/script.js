function openTab (evt, tabName){
    //find all the tabs and hide them
 const tabcontent = document.querySelectorAll(".tabcontent"); //returns all non-live nodelist
 tabcontent.forEach(el => el.style.display="none");

 //find all tab-buttons and remove active class
  const tablinks = document.querySelectorAll(".tablinks");
  tablinks.forEach(el =>el.classList.remove("active"));

  // show selected tab
  document.getElementById(tabName).style.display="block";

  //give class active class for css styling
  evt.currentTarget.classList.add("active");

}

//when loading innto the site the first tab should open autromatically

document.addEventListener("DOMContentLoaded", () => {
 document.querySelector(".tablinks").click();
});
