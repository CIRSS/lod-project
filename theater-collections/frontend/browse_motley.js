let url_string = window.location.href;
let url = new URL(url_string);
let page = url.searchParams.get("page");
if (page === null) {
    page = 1;
}

let empty_page_url = "http://imagesearch-test1.library.illinois.edu/browse_motley.html?page=";

if (page > 1) {
    $("#top_nav").prepend("<a href='" + empty_page_url + (page-1) + "'>&lt; Prev</a>");
    $("#bottom_nav").prepend("<a href='" + empty_page_url + (page-1) + "'>&lt; Prev</a>");

    $("#top_nav").append("<a href='" + empty_page_url + "1'>1</a>");
    $("#bottom_nav").append("<a href='" + empty_page_url + "1'>1</a>");
}

if (page > 5) {
    $("#top_nav").append("...");
    $("#bottom_nav").append("...");
}

for (let i = (page > 4 ? page - 3 : 2); i < page; i++) {
    $("#top_nav").append("<a href='" + empty_page_url + i + "'>" + i + "</a>");
    $("#bottom_nav").append("<a href='" + empty_page_url + i + "'>" + i + "</a>");
}

$("#top_nav").append(" <span style='font-weight: bold;'>" + page + "</span> ");
$("#bottom_nav").append(" <span style='font-weight: bold;'>" + page + "</span> ");

let search_query = 'http://imagesearch-test1.library.illinois.edu/solrproxy/getsolrresult.asp?q=*:*&fl=search_title,search_performance,search_theater,splashUrl,thumbUrl&sort=search_performance asc,search_title asc&rows=25&start=' + (page-1)*25;

$.get(search_query, function(data) {
    for (let i = 1; i <= 3 && parseInt(page) + i <= Math.floor(data.response.numFound/25)+1; i++) {
        $("#top_nav").append("<a href='" + empty_page_url + (parseInt(page)+i) + "'>" + (parseInt(page)+i) + "</a>");
        $("#bottom_nav").append("<a href='" + empty_page_url + (parseInt(page)+i) + "'>" + (parseInt(page)+i) + "</a>");
    }

    if (Math.floor(data.response.numFound/25)+1 - page > 4) {
        $("#top_nav").append("...");
        $("#bottom_nav").append("...");
    }

    if (Math.floor(data.response.numFound/25)+1 - page > 3) {
        $("#top_nav").append("<a href='" + empty_page_url + parseInt(Math.floor(data.response.numFound/25)+1) + "'>" + parseInt(Math.floor(data.response.numFound/25)+1) + "</a>");
        $("#bottom_nav").append("<a href='" + empty_page_url + parseInt(Math.floor(data.response.numFound/25)+1) + "'>" + parseInt(Math.floor(data.response.numFound/25)+1) + "</a>");
    }

    if (page < Math.floor(data.response.numFound/25)+1) {
        $("#top_nav").append("<a href='" + empty_page_url + (parseInt(page)+1) + "'>Next &gt;</a>");
        $("#bottom_nav").append("<a href='" + empty_page_url + (parseInt(page)+1) + "'>Next &gt;</a>");
    }

    let items = data.response.docs;
    for (let i = 0; i < items.length; i++) {
        let performance = "<a href='http://imagesearch-test1.library.illinois.edu/browse_group.html?g=performance&t=" + items[i]['search_performance'].replace(/'/g,"&#39;") + "'  class='browse_link'>" + items[i]['search_performance'] + "</a>";
        let theater = (typeof items[i]['search_theater'] !== "undefined" ? "<a href='http://imagesearch-test1.library.illinois.edu/browse_group.html?g=theater&t=" +  items[i]['search_theater'][0].replace(/'/g,"&#39;") + "'  class='browse_link'>" + items[i]['search_theater'][0] + "</a>" : "");
        let item = "<a href='" + items[i]['splashUrl'] + "' class='browse_link' style='font-weight: bold; font-size: 14px;'>" + items[i]['search_title'] + "</a>";
        let thumbnail = "<a href='" + items[i]['splashUrl'] + "'><img src='" + items[i]['thumbUrl'].substring(0,items[i]['thumbUrl'].length-4) + ".jpg' class='browse_thumb' /></a>";
        $("#item_table").append("<li>" + thumbnail + "<ul style='list-style-type: none; position: relative; top: 25px;'><li>" + item + "</li><li><span style='font-weight: bold;'>Performance Title:</span> " + performance + "</li><li><span style='font-weight: bold;'>Theater:</span> " + theater + "</li></ul><hr size='1px' style='clear: left; margin-top: 0px; margin-bottom: 0px;'></li>");
    }
});