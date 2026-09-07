// The code of this file is for the mobile view of the web pages
// The code was written by the author (Student No.: 200212427 of the University of London) of the project, and was used on the website <howa.space> that was written and owned by the same author.

let is_mobile = false;
let is_menu_open = false;

const menu_button = document.getElementById("menu_button");

const browser_resizing = () => {
    is_mobile = window.innerWidth < 800 ? true : false;
    // update mobile menu  
    mobile_menu_update(is_mobile, is_menu_open);
};

window.addEventListener("load", browser_resizing);
window.addEventListener("resize", browser_resizing);

menu_button.addEventListener('mouseup', () => {
    is_menu_open = !is_menu_open;
    mobile_menu_update(is_mobile, is_menu_open);
});

const mobile_menu_update = (is_mobile, is_menu_open) => {
    // update the mobile menu
    const a_in_menu = document.querySelectorAll("#menu a");
    const div_a_in_menu = document.querySelectorAll("#menu div a");
    const div_in_menu = document.querySelectorAll("#menu div");
    const menu = document.getElementById("menu");
    if (is_menu_open && is_mobile)
    {
        menu.style.display = "block";
        for (const a of a_in_menu) a.style.display = "block";
        for (const div_a of div_a_in_menu) div_a.style.display = "block";
        for (const div of div_in_menu)
        {
            div.style.display = "block";
            div.style.float = "none";
        }
    }
    else if (!is_mobile)
    {
        menu.style.display = "inline";
        for (const a of a_in_menu) a.style.display = "inline";
        for (const div_a of div_a_in_menu) div_a.style.display = "inline";
        for (const div of div_in_menu)
        {
            div.style.display = "inline";
            div.style.float = "right";
        }
    }
    else
    {
        menu.style.display = "none";
    }

    // update the menu and menu button
    menu_button.style.display = is_mobile ? "block" : "none";
};