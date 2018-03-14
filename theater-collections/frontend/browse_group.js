searchLiteral = function(literals, locale) {
    if (literals !== undefined) {
        for (i = 0; i < literals.length; i++) {
            if (literals[i]['lang'] === locale) {
                return literals[i]['value'];
            }
        };
    }
    return undefined;
};

cutString = function(words, charcount) {
    var tempwords = '';
    //console.log(words+':'+charcount);
    i = 0;
    if (words !== undefined) {
        while (i < words.length && (i < charcount || (i >= charcount && words[i] != ' '))) {
            tempwords = tempwords + words[i];
            i++;
        }
    }
    //console.log(tempwords);
    return tempwords;
};

function getWikiData(wiki_url,callback) {
    var apiUrl = wiki_url.replace('https://en.wikipedia.org/wiki','http://imagesearch-test1.library.illinois.edu/dbpedia/data') + '.json';
    console.log('Wiki url: ' + apiUrl);

    $.get(apiUrl, function(jsonData) {
        //parse wiki url content to get title
        var splitUrl = wiki_url.split('/');
        var title = splitUrl[splitUrl.length - 1];
        var dbpediaUrl = decodeURIComponent('http://dbpedia.org/resource/' + title);
        var jsonReference = encodeURI(dbpediaUrl);

        if (!(jsonReference in jsonData)) {
            if (dbpediaUrl in jsonData) {
                jsonReference = dbpediaUrl;
            }
            else {
                return false;
            }
        }

        //getabstratct from json
        var abstracts = undefined
        if ('http://www.w3.org/2000/01/rdf-schema#comment' in jsonData[jsonReference]) {
            abstracts = jsonData[jsonReference]['http://www.w3.org/2000/01/rdf-schema#comment'];
        }
        var myAbstract = "";
        var shortAbstract = ""
        //getname
        var myNames = undefined
        if ('http://www.w3.org/2000/01/rdf-schema#label' in jsonData[jsonReference]) {
            myNames = jsonData[jsonReference]['http://www.w3.org/2000/01/rdf-schema#label'];
        }
        var myName = "";

        var wikiThumbnail = undefined;
        if ('http://dbpedia.org/ontology/thumbnail' in jsonData[jsonReference]) {
            wikiThumbnail = jsonData[jsonReference]['http://dbpedia.org/ontology/thumbnail'];
        }

        if (myNames !== undefined) {
            myName = searchLiteral(myNames, 'en');
        }

        if (abstracts !== undefined) {
            myAbstract = searchLiteral(abstracts, 'en');

            //console.log(myAbstract);
            //shortAbstract = cutString(myAbstract, charCount) + ' <a href="' + wiki_url + '" class="newwindow">[more from Wikipedia]</a>';
            shortAbstract = cutString(myAbstract, 250);
        }
        var wikiData = {
            title: myName,
            longAbstract: myAbstract,
            shortAbstract: shortAbstract,
            dbpediaUrl: dbpediaUrl,
            resource: jsonData[jsonReference],
            wiki_url: wiki_url,
            wiki_thumb: wikiThumbnail
        };
        
        var viafUrl = ''
        for (grouping in wikiData.resource) {
            if ((wikiData.resource[grouping][0]['type'] === 'uri')) {// && (wikiData.resource[grouping][0]['value'].search('viaf.org') >= 0) {
                for (var i=0; i < wikiData.resource[grouping].length; i++) {
                    if (wikiData.resource[grouping][i]['type'] === 'uri' && wikiData.resource[grouping][i]['value'].search('viaf.org') >= 0) {
                        viafUrl = wikiData.resource[grouping][i]['value']
                    }
                }
            }
        }

        var result = { viafUrl: viafUrl, wikiData: wikiData };
//			console.log(result);
        (callback ? callback(result) : false);
    });
}

function getExternalLinkLabel(url) {
    if (url.includes('theatricalia.com')) {
        return "Theatricalia";
    }
    else if (url.includes('worldcat.org/identities')) {
        return "WorldCat Identities";
    }
    else if (url.includes('imdb.com')) {
        return "IMDb";
    }
    else if (url.includes('en.wikipedia.org')) {
        return "Wikipedia";
    }
    else if (url.includes('viaf.org')) {
        return "VIAF Record";
    }
    else if (url.includes('id.loc.gov')) {
        return "LC Record";
    }
    else if (url.includes('ibdb.com')) {
        return "IBDB";
    }
    else {
        return "Other";
    }
}

function augmentInfoboxWithWikipedia(target_url,group) {
    getWikiData(target_url,function(returned_content) {
        if (returned_content.wikiData.wiki_thumb !== undefined) {
            console.log(returned_content.wikiData.wiki_thumb);
            $("#info_box").prepend("<a href='" + returned_content.wikiData.wiki_url + "'><img src='" + returned_content.wikiData.wiki_thumb[0]['value'].replace(/'/g,"&#39;") + "' id='ib_image' /></a>");
        }

        if (returned_content.wikiData.shortAbstract.length > 0) {
            $("#ib_title").after("<div id='wiki_blurb'>" + returned_content.wikiData.shortAbstract + " <a href='" + returned_content.wikiData.wiki_url + "'>[more from Wikipedia]</a></div>");
        }
        console.log(returned_content);
    });

    console.log('Links query: ' + 'http://imagesearch-test1.library.illinois.edu/xmlSparql/getName.asp?' + encodeURIComponent(target_url));
    $.get('http://imagesearch-test1.library.illinois.edu/xmlSparql/getName.asp?' + encodeURIComponent(target_url).replace(/'/g,"%2527"), function(data) {
        if (data.results.bindings.length > 0) {
            $("#external_title").after("<ul id='external_list'></ul>");
            for (var i = 0; i < data.results.bindings.length; i++) {
                if (data.results.bindings[i].sameAs.value !== target_url) {
                    $("#external_list").append("<li class='text_col" + ((i % 3) + 1) + "'><a href='" + data.results.bindings[i].sameAs.value + "'>" + getExternalLinkLabel(data.results.bindings[i].sameAs.value) + "</a></li>");
                }
            }
            if ($("#external_list").is(':empty')) {
                $("#external_title").remove();
            }
        }
        else {
            $("#external_title").remove();
        }
    });

    console.log('Sent URL: http://imagesearch-test1.library.illinois.edu/xmlSparql/getName.asp?' + (group == 'theater' ? '@' : '$') + encodeURIComponent(target_url).replace(/'/g,"%2527"));
    $.get('http://imagesearch-test1.library.illinois.edu/xmlSparql/getName.asp?' + (group == 'theater' ? '@' : '$') + encodeURIComponent(target_url).replace(/'/g,"%2527"), function(data) {
        console.log(data);
        if (data.results.bindings.length > 0) {
            $("#related_people_title").after("<ul id='related_people_list'></ul>");
            for (var i = 0; i < data.results.bindings.length; i++) {
                getWikiData(data.results.bindings[i].sameAs.value, function(returned_content) {
                    console.log(returned_content);
                    $("#related_people_list").append("<li class='rp_column" + ((($("#related_people_list > li").length) % 3)+1) + "'><a href='" + returned_content.wikiData.wiki_url + "'><img src='" + (returned_content.wikiData.wiki_thumb !== undefined ? returned_content.wikiData.wiki_thumb[0].value.replace(/'/g,"&#39;") : '/ui/custom/default/collection/default/images/no_image.png' ) + "' class='person_thumb'></br>" + returned_content.wikiData.title + "</a></li>");
                });
            }
        }
        else {
            $("#related_people_title").remove();
        }
    });
}

function createInfocard(group,target) {
    let anti_group = (group === 'theater' ? 'performance' : 'theater' );
    let split_position = target.indexOf('<');
    if (split_position > -1) {
        var target_name = target.substring(0,split_position);
        var target_url = target.substring(split_position+1,target.length-1);
        var anti_group_query = 'http://imagesearch-test1.library.illinois.edu/solrproxy/getsolrresult.asp?q=search_' + group + ':"' + target.substring(0,split_position) + target.substring(split_position).replace(/'/g,"%2527") + '"&fl=search_' + anti_group + '&facet=on&facet.field=search_' + anti_group + '&facet.sort=count&rows=0';
    }
    else {
        var target_name = target;
        var anti_group_query = 'http://imagesearch-test1.library.illinois.edu/solrproxy/getsolrresult.asp?q=search_' + group + ':"' + target_name + '"&fl=search_' + anti_group + '&facet=on&facet.field=search_' + anti_group + '&facet.sort=count&rows=0';
    }
    document.title = target_name;

    $("<div id='info_box'></div>").insertBefore("#item_table");
    $("#info_box").append("<div id='ib_title'>" + target_name + "</div>");
    $("#info_box").append("<div id='related_title' class='ib_subhead'>Related " + anti_group.replace(/\b[a-z]/g, function(letter) { return letter.toUpperCase(); }) + "s in Collection</div>");
    $("#info_box").append("<div id='related_people_title' class='ib_subhead'>Related People on Wikipedia</span></div>");
    $("#info_box").append("<div id='external_title' class='ib_subhead'>External Links</div>");

    if (target_url !== undefined) {
        augmentInfoboxWithWikipedia(target_url,group);
    }
    else {
        $.get('http://imagesearch-test1.library.illinois.edu/xmlSparql/getName.asp?' + target_name,function (data) {
            if (data.results.bindings[0].id.value !== undefined) {
                augmentInfoboxWithWikipedia(data.results.bindings[0].id.value,group);
            }
        });
    }

    $.get(anti_group_query, function(data) {
        let items = data.facet_counts.facet_fields['search_' + anti_group];
        if ( items.length > 0 ) {
            $("#related_title").after("<ul id='related_list'></ul>")
            for (let i = 0; i < items.length && items[i+1] > 0; i+=2) {
                $("#related_list").append("<li><a href='http://imagesearch-test1.library.illinois.edu/browse_group.html?g=" + anti_group + "&t=" + items[i].replace(/'/g,"&#39;") + "'>" + items[i] + "</a></li>")
            }
            if ($("#related_list").is(':empty')) {
                $("#related_title").remove();
            }
        }
        else {
            $("#related_title").remove();
        }
        console.log(items);
    });
}

let url_string = window.location.href;
let url = new URL(url_string);
let group = url.searchParams.get("g");
let target = url.searchParams.get("t");
if (group !== null && target !== null) {
    createInfocard(group,target);

    let page = url.searchParams.get("page");
    if (page === null) {
        page = 1;
    }

    let empty_page_url = "http://imagesearch-test1.library.illinois.edu/browse_group.html?g=" + group + "&t=" + target.replace(/'/g,"&#39;") + "&page=";

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

    let search_query = 'http://imagesearch-test1.library.illinois.edu/solrproxy/getsolrresult.asp?fl=search_title,search_performance,search_theater,splashUrl,thumbUrl&sort=search_performance asc,search_title asc&rows=25&start=' + (page-1)*25;

    if (group === 'performance') {
        $("#breadcrumb_top_content").append('<a href="/browse_by.html?g=performance" class="action_link_10" tabindex="18"> Performances</a> <img src="/ui/cdm/default/collection/default/css/images/double_arrow_e.png" alt="arrow" /> ' + target);
        let link_start_index = target.indexOf('<');
        if (link_start_index > -1) {
            search_query += '&q=search_performance:"' + target.substring(0,link_start_index) + target.substring(link_start_index).replace(/'/g,"%2527") +'"';
        }
        else {
            search_query += '&q=search_performance:"' + target +'"';
        }
    }
    else {
        $("#breadcrumb_top_content").append('<a href="/browse_by.html?g=theater" class="action_link_10" tabindex="18"> Theaters</a> <img src="/ui/cdm/default/collection/default/css/images/double_arrow_e.png" alt="arrow" /> ' + target);
        let link_start_index = target.indexOf('<');
        if (link_start_index > -1) {
            search_query += '&q=search_theater:"' + target.substring(0,link_start_index) + target.substring(link_start_index).replace(/'/g,"%2527") +'"';
        }
        else {
            search_query += '&q=search_theater:"' + target + '"';
        }
    }

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
            let performance = ( group === 'performance' ? items[i]['search_performance'] : "<a href='http://imagesearch-test1.library.illinois.edu/browse_group.html?g=performance&t=" + items[i]['search_performance'].replace(/'/g,"&#39;") + "'  class='browse_link'>" + items[i]['search_performance'] + "</a>");
            let theater = (typeof items[i]['search_theater'] === "undefined" ? "" : ( group === 'theater' ? items[i]['search_theater'][0] : "<a href='http://imagesearch-test1.library.illinois.edu/browse_group.html?g=theater&t=" +  items[i]['search_theater'][0].replace(/'/g,"&#39;") + "'  class='browse_link'>" + items[i]['search_theater'][0] + "</a>" ));
            let item = "<a href='" + items[i]['splashUrl'] + "' class='browse_link' style='font-weight: bold; font-size: 14px;'>" + items[i]['search_title'] + "</a>";
            let thumbnail = "<a href='" + items[i]['splashUrl'] + "'><img src='" + items[i]['thumbUrl'].substring(0,items[i]['thumbUrl'].length-4) + ".jpg' class='browse_thumb' /></a>";
            $("#item_table").append("<li>" + thumbnail + "<ul style='list-style-type: none; position: relative; top: 25px;'><li>" + item + "</li><li><span style='font-weight: bold;'>Performance Title:</span> " + performance + "</li><li><span style='font-weight: bold;'>Theater:</span> " + theater + "</li></ul><hr size='1px' style='clear: left; margin-top: 0px; margin-bottom: 0px;'></li>");
        }
    });
}