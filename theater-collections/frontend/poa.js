ready_function = function() {
/*	 $('.description_col2').each(function() {
		// Turn URLs in CONTENTdm HTML into hyperlink anchors 
		if (this.firstChild != null && $.trim(this.firstChild.nodeValue) == '') {

			$(this).find('br').replaceWith('<span>;</span>');
			var html = '';
			var terms = this.innerText.split(';');
			//console.log(terms);
			terms.forEach(function(term, index) {
				var link = '';
				if (term.includes('<')) {
					link = term.substring(term.indexOf('<') + 1);
					link = link.substring(0, link.indexOf('>') - 1)
					term = term.substring(0, term.indexOf('<') - 1);
				}

				if (term.startsWith('http://') || term.startsWith('https://')) {
					if (term.includes('/rdfa/')) {
						term = term.replace('rdfa','jsonld').replace('html','json');
					} else if (term.includes('.jp2')) {
						term = term.replace(/jp2/g,'jpg');
					}
					html = html + '<a class="body_link_11" href="' + term + '">' + term + '</a>';
				} else {
					html = html + '<a class="body_link_11" href="/cdm/search/searchterm/' + term + '">' + term + '</a>';
				}

				if (link != '') {
					if (link.includes('viaf.org')) {
						html = html + '<a title="VIAF Record" href=' + link + '>';
						html = html + '<span class="icon_11 ui-icon-extlink"></span>';
						html = html + '</a>';
					} else if (link.includes('wikipedia.org')) {
						html = html + '<a title="Wikipedia" href=' + link + '>';
						html = html + '<span class="icon_11 ui-icon-extlink"></span>';
						html = html + '</a>';
					} else if (link.includes('theatricalia.com')) {
						html = html + '<a title="Theatricalia" href=' + link + '>';
						html = html + '<span class="icon_11 ui-icon-extlink"></span>';
						html = html + '</a>';
					} else if (link.includes('http://id.loc.gov')) {
						html = html + '<a title="Library of Congress Vocabularies" href=' + link + '>';
						html = html + '<span class="icon_11 ui-icon-extlink"></span>';
						html = html + '</a>';
					} else if (link.includes('getty.edu')) {
						html = html + '<a title="Getty Vocabularies" href=' + link + '>';
						html = html + '<span class="icon_11 ui-icon-extlink"></span>';
						html = html + '</a>';
					} else {
						html = html + '<a href=' + link + '>';
						html = html + '<span class="icon_11 ui-icon-extlink"></span>';
						html = html + '</a>';
					}
				}
				html = html + '<br/>';
			});

			this.innerHTML = html;
		}
	});*/
	
	$('.description_col1').each(function() {
		var term = this.innerText;
		if (term == 'JPEG2000 URL') {
			term = 'JPG URL';
		} else if (term == 'RDFa') {
			term = 'RDF';
		}
		
		this.innerText = term;
	});

	// Initialize global constants
	locale = 'en';
	charCount = 250;

	// Utility functions
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

	getObjectWithAttr = function(object, attr) {
		for (i = 0; i < object.length; i++) {
			if (object[i][attr] !== undefined) {
				return object[i];
			}
		}
		return undefined;
	};

	renderLinks = function(links, label) {
		var content = '';
		if (Array.isArray(links)) {
			for (i = 0; i < links.length; i++) {
				var link = links[i];
				content = content + '<br/><a href="' +
					link + '" class="newwindow">' + label;
				if (links.length > 1) {
					content = content + '-' + (i + 1) + '</a>'
				} else {
					content = content + '</a>'
				}
			}
		} else {
			content = content + '<br/><a href="' +
				links + '" class="newwindow">' + label + '</a>';
		}
		return content;
	}

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

	// AutomapperConfig Prototype
	AutomapperConfig = function() {
		//this.enWikiUrl = [];
		this.dbpediaUrl = '';        
		this.VIAFLink = [];
		this.BNFLinks = [];
		this.DNBLinks = [];
		this.worldCatIdUrl = [];
		this.theatricaliaUrl = [];
		this.imdbUrl = [];
		this.ibdbUrl = [];
		this.sameAs = [];
	}

	// Prototypes (suedo-class) for linked data entities - people, performances / plays, theaters
	//   Not particularly useful in JavaScript, but helpful for documenting and keeping code straight
	// TODO: Need to separate plays (as in script) from performances (an event)
	function PerformanceEntity(id, identifier, homePage, longAbstract, shortAbstract, name, enWikiUrl, ViafUrl, premiere, playSubject) {
		this.id = id;
		this.identifier = identifier;
		this.homePage = homePage;
		this.longAbstract = longAbstract;
		this.shortAbstract = shortAbstract;
		this.name = name;
		this.enWikiUrl = enWikiUrl;
		this.ViafUrl = ViafUrl;
		this.links = new AutomapperConfig ();
		this.type = 'Performance';
		this.premiere = premiere;
		this.playSubject = playSubject;    	
		return;
	}
	
	function PersonEntity(id, identifier, homePage, longAbstract, shortAbstract, name, enWikiUrl, ViafUrl, jobTitle, gender, birthDate, deathDate) {
		this.id = id;
		this.identifier = identifier;
		this.homePage = homePage;
		this.longAbstract = longAbstract;
		this.shortAbstract = shortAbstract;
		this.name = name;
		this.enWikiUrl = enWikiUrl;
		this.ViafUrl = ViafUrl;
		this.links = new AutomapperConfig ();
		this.type = 'Person';    	
		this.jobTitle = ( jobTitle ? jobTitle :  'Actor' );    	
		this.gender = gender;
		this.birthDate = birthDate;
		this.deathDate = deathDate;    	
		return;
	}
	
	function TheaterEntity(id, identifier, homePage, longAbstract, shortAbstract, name, enWikiUrl, ViafUrl, address, openingYear, seatingCapacity) {
		this.id = 'theater-' + id;
		this.identifier = identifier;
		this.homePage = homePage;
		this.longAbstract = longAbstract;
		this.shortAbstract = shortAbstract;
		this.name = name;
		this.enWikiUrl = enWikiUrl;
		this.ViafUrl = ViafUrl;
		this.links = new AutomapperConfig ();
		this.type = 'PerformingArtsTheater';
		this.address = address;
		this.openingYear = openingYear;
		this.seatingCapacity = seatingCapacity; 
		return;
	}
	
  function viafModel () {
      this.Name = '' ;
      this.Gender = 'unknown' ;
      this.BirthDate = 0 ;
      this.DeathDate = 0 ;
      this.DNBLinks = [] ;
      this.VIAFLink = '' ;
      this.BNFLinks = [] ;
      this.Wikipedia = [] ;
  }
	
	getViafContent = function(viafUrl, callback, errorcallback) {
		//get dbpedia link using jquery ajax request
		if (viafUrl === undefined) {
			var result = {
				error: true,
				msg: 'viafurl is not defined'
			};
			(errorcallback ? errorcallback(result) : (callback ? callback(result) : false));

			return;
		}

		if (viafUrl.search('viaf.org') < 0) {
			var result = {
				error: true,
				msg: 'not a viafurl'
			};
			(errorcallback ? errorcallback(result) : (callback ? callback(result) : false));

			return;
		}

		var vData = new viafModel() ;
		//console.log(viafUrl) ;
		var viafUrlX = viafUrl.replace('http://viaf.org/','http://imagesearch-test1.library.illinois.edu/') + '/marc21.xml' ;
		var viafUrlJ = viafUrl.replace('http://viaf.org/','http://imagesearch-test1.library.illinois.edu/') + '/justlinks.json' ;
    
    	var viafX = $.ajax({
			type: "GET", 
			//url: "http://imagesearch-test1.library.illinois.edu/marc21.xml",
			url: viafUrlX ,
			dataType: "xml", 
			success: function(vXml) {
				var xmlNode = $( vXml ).find ('mx\\:record mx\\:datafield[tag="700"] mx\\:subfield[code="a"]' );
				if (xmlNode.length == 0 ) {
					xmlNode = $( vXml ).find ('mx\\:record mx\\:datafield[tag="710"] mx\\:subfield[code="a"]' );
				}
				if (xmlNode.length == 0 ) {
					xmlNode = $( vXml ).find ('mx\\:record mx\\:datafield[tag="720"] mx\\:subfield[code="a"]' );
				}
				//console.log ($(xmlNode).eq(0).text()) ;
				vData.Name = $(xmlNode).eq(0).text() ;

				xmlNode = $( vXml ).find ('mx\\:record mx\\:datafield[tag="375"] mx\\:subfield[code="a"]' );
				if (xmlNode.length > 0 ) {
					vData.Gender = $(xmlNode).eq(0).text() ;
				}

				xmlNode = $( vXml ).find ('mx\\:record mx\\:datafield[tag="997"] mx\\:subfield[code="a"]' );
				if (xmlNode.length > 0 ) {
					vData.BirthDate = $(xmlNode).eq(0).text() ;
				}

				xmlNode = $( vXml ).find ('mx\\:record mx\\:datafield[tag="997"] mx\\:subfield[code="b"]' );
				if (xmlNode.length > 0 ) {
					vData.DeathDate = $(xmlNode).eq(0).text() ;
				}
			},
			error: function(xhr,status,errorthrown) {
				var result = {
					error: true,
					msg: 'no viaf xml at that url'
				};
				(errorcallback ? errorcallback(result) : (callback ? callback(result) : false));
	
				return;
			}
		}) ;
    
		var viafJ = $.ajax( {
			type: "GET",
			//url:  "http://imagesearch-test1.library.illinois.edu/justlinks.json",
			url: viafUrlJ ,
			dataType: "json",
			success: function(vJson) {
				vData.BNFLinks = vJson.BNF ;
				vData.DNBLinks =  vJson.DNB  ;
				vData.Wikipedia = vJson.Wikipedia ;
				vData.VIAFLink = "https://viaf.org/viaf/" + vJson.viafID  ; 
				//console.log(vData.VIAFLink) ;
			},
			error: function(xhr,status,errorthrown) {
				var result = {
					error: true,
					msg: 'no viaf json at that url'
				};
				(errorcallback ? errorcallback(result) : (callback ? callback(result) : false));
	
				return;
			}
		});    
    

//		var apiUrl = 'http://imagesearch-test1.library.illinois.edu/VIAFProxy/api/name?url=' + viafUrl + '&type=json';
//		var apiUrl = viafUrl;
//		$.get(apiUrl, function(data) {
//			var jsonData = data;
			// getWiki content
//      var wikis = jsonData['Wikipedia'];

		$.when(viafX, viafJ).done ( function() {    
			// getWiki content
			// console.log(vData) ;
			var wikis = $( vData.Wikipedia ) ;
     		 var wikiUrl = '';
			for (i = 0; i < wikis.length; i++) {
				if (wikis[i].search('en.wikipedia') >= 0) {
					wikiUrl = wikis[i];
					//break immediate
					break;
				}
			}
			//console.log(wikiUrl) ;
			
			var result = { wikiUrl: wikiUrl, viafData: vData };
			(callback ? callback(result) : false);
		});
	};
	
	//gedbpedia content from wikipedia url
	getDbPediaContent = function(wikiUrl, callback, errorcallback) {
		if (wikiUrl === undefined) {
			var result = {
				error: true,
				msg: 'wikipedia url is not defined'
			};
			(errorcallback ? errorcallback(result) : (callback ? callback(result) : false));

			return;
		}

		if (wikiUrl.search('wikipedia.org') < 0) {
			var result = {
				error: true,
				msg: 'not a wikipedia url'
			};
			(errorcallback ? errorcallback(result) : (callback ? callback(result) : false));

			return;
		}
//  *** modified lines 266 through 275 to use reverse proxy rather than dedicated VB.Net proxy
//  *** Typically dbpedia.org/data includes "access-control-allow-origin": "*" obviating need for proxy, but not always and reverse proxy implements local server caching...
//		var apiUrl = 'http://imagesearch-test1.library.illinois.edu/DBPediaProxy/home/entity?url=' + wikiUrl;
		var apiUrl = wikiUrl.replace('https://en.wikipedia.org/wiki','http://imagesearch-test1.library.illinois.edu/dbpedia/data') + '.json';
//		var apiUrl = wikiUrl.replace('https://en.wikipedia.org/wiki','http://dbpedia.org/data') + '.json';

		//console.log(apiUrl);

		$.get(apiUrl, function(jsonData) {
		    //console.log (data) ;
			//var jsonData = JSON.parse(data);
			//var jsonData = data ;
			//parse wiki url content to get title
			var splitUrl = wikiUrl.split('/');
			//console.log(JSON.stringify(splitUrl));
			var title = splitUrl[splitUrl.length - 1];
			//console.log(title);
			var dbpediaUrl = decodeURIComponent('http://dbpedia.org/resource/' + title);
			var jsonReference = encodeURI(dbpediaUrl)
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

			if (myNames !== undefined) {
				myName = searchLiteral(myNames, locale);
			}

			if (abstracts !== undefined) {
				myAbstract = searchLiteral(abstracts, locale);

				//console.log(myAbstract);
				//shortAbstract = cutString(myAbstract, charCount) + ' <a href="' + wikiUrl + '" class="newwindow">[more from Wikipedia]</a>';
				shortAbstract = cutString(myAbstract, charCount);
			}
			var wikiData = {
				title: myName,
				longAbstract: myAbstract,
				shortAbstract: shortAbstract,
				dbpediaUrl: dbpediaUrl,
				resource: jsonData[jsonReference],
				wikiUrl: wikiUrl
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
	};	
	
	grabContentFromWeb = function(wikiUrl, viafUrl, callback) {
		var result = { wikiUrl: wikiUrl, viafUrl: viafUrl }
		if (wikiUrl === undefined) {
			var order_of_operations = [getViafContent, getDbPediaContent]
			var ordered_inputs = ['viafUrl', 'wikiUrl']
		} else {
			var order_of_operations = [getDbPediaContent, getViafContent]
			var ordered_inputs = ['wikiUrl', 'viafUrl']
		}
		
		var promises = []
		
		var i = 0;
		promises.push((function(i) {
			var dfd = $.Deferred();
			order_of_operations[0](result[ordered_inputs[0]],function(returned_content) {
				if (!('error' in returned_content)) {
					result[ordered_inputs[0].substring(0,4) + 'Data'] = returned_content[ordered_inputs[0].substring(0,4) + 'Data'];
					if ((result[ordered_inputs[1]] === undefined) && (returned_content[ordered_inputs[1]] != '')) {
						result[ordered_inputs[1]] = returned_content[ordered_inputs[1]]
					}
				}
				dfd.resolve();
			});

			return dfd.promise();
		})(i));
		
		$.when(promises[0]).then(function() {
			order_of_operations[1](result[ordered_inputs[1]],function(returned_content) {
				if (!('error' in returned_content)) {
					result[ordered_inputs[1].substring(0,4) + 'Data'] = returned_content[ordered_inputs[1].substring(0,4) + 'Data'];
				}
				
				(callback ? callback(result) : false);
			});
		});
	};


	function accordionObject(id,jobTitle,name,address,birthdate,dbpediaUrl,deathdate,enWikiUrl,gender,homePage,VIAFLink,BNFLink,DNBLink,worldCatIdUrl,theatricaliaUrl,imdbUrl,ibdbUrl,sameAs,longAbstract,openingYear,playSubject,premiere,seatingCapacity,shortAbstract) {
		this.id = id;
		this.jobTitle = jobTitle;
		this.name = name;
		this.address = address;
		this.birthdate = birthdate;
		this.dbpediaUrl = dbpediaUrl;
		this.deathdate = deathdate;
		this.enWikiUrl = enWikiUrl;
		this.gender = gender;
		this.homePage = homePage;
		this.links = {};
		this.links.VIAFLink = VIAFLink;
		this.links.BNFLink = BNFLink;
		this.links.DNBLink = DNBLink;
		this.links.worldCatIdUrl = worldCatIdUrl;
		this.links.theatricaliaUrl = theatricaliaUrl;
		this.links.imdbUrl = imdbUrl;
		this.links.ibdbUrl = ibdbUrl;
		this.links.sameAs = sameAs;
		this.longAbstract = longAbstract;
		this.openingYear = openingYear;
		this.playSubject = playSubject;
		this.premiere = premiere;
		this.seatingCapacity = seatingCapacity;
		this.shortAbstract = shortAbstract;
		this.if_jobTitle = jobTitle ? true : false;
		this.if_address = address ? true : false;
		this.if_birthdate = birthdate ? true : false;
		this.if_dbpediaUrl = dbpediaUrl ? true : false;
		this.if_deathdate = deathdate ? true : false;
		this.if_enWikiUrl = enWikiUrl ? true : false;
		this.if_gender = (gender && gender !== 'unknown') ? true : false;
		this.if_homePage = homePage ? true : false;
		this.if_longAbstract = longAbstract ? true : false;
		this.if_openingYear = openingYear ? true : false;
		this.if_playSubject = playSubject ? true : false;
		this.if_premiere = premiere ? true : false;
		this.if_seatingCapacity = seatingCapacity ? true : false;
		this.if_shortAbstract = shortAbstract ? true : false;
		this.if_links_without_shortAbstract = (this.if_shortAbstract == false && (VIAFLink || BNFLink || DNBLink || worldCatIdUrl || theatricaliaUrl || imdbUrl || ibdbUrl || sameAs || dbpediaUrl)) ? true : false;
		this.if_BNFLink = BNFLink ? true : false;
		this.if_DNBLink = DNBLink ? true : false;
		this.if_ibdbUrl = ibdbUrl ? true : false;
		this.if_imdbUrl = imdbUrl ? true : false;
		this.if_theatricaliaUrl = theatricaliaUrl ? true : false;
		this.if_sameAs = sameAs ? true : false;
		this.if_VIAFLink = VIAFLink ? true : false;
		this.if_worldCatIdUrl = worldCatIdUrl ? true : false;
		return;
	}

	wrapWindow = function(params,callback1, callback2) {
		console.log(params)

		var output = Mustache.render(`
			<div id="{{id}}" style="margin-bottom: 10px">
				<h2 class="sidebar_accordion_header accordion_header ui-accordion-header ui-helper-reset accordion_header_open ui-state-active ui-corner-top ui-state-focus">
					<span class="accordion_header_icon ui-icon ui-sidebar-icon-triangle-1-s sidebar_accordion_header_icon_open"></span>
					{{name}}{{#if_jobTitle}} ({{jobTitle}}){{/if_jobTitle}}
				</h2>
				<div class="sidebar_accordion_window accordion_window ui-accordion-content ui-helper-reset ui-widget-content ui-corner-bottom ui-accordion-content-active">
					<p>
					<ul style="padding-left: 10px;">
						{{#if_address}}
						<li>Address: {{address}}</li>
						{{/if_address}}
						{{#if_seatingCapacity}}
						<li>Seating Capacity: {{seatingCapacity}}</li>
						{{/if_seatingCapacity}}
						{{#if_openingYear}}
						<li>Opening Year: {{openingYear}}</li>
						{{/if_openingYear}}
						{{#if_homePage}}
						<li><a href="{{homePage}}" class="newwindow">Homepage</a></li>
						{{/if_homePage}}
						{{#if_gender}}
						<li>Gender: {{gender}}</li>
						{{/if_gender}}
						{{#if_birthdate}}
						<li>Birth Date: {{birthdate}}</li>
						{{/if_birthdate}}
						{{#if_deathdate}}
						<li>Death Date: {{deathdate}}</li>
						{{/if_deathdate}}
						{{#if_premiere}}
						<li>Premiere: {{premiere}}</li>
						{{/if_premiere}}
						{{#if_playSubject}}
						<li>Subject of Play: {{playSubject}}</li>
						{{/if_playSubject}}
					</ul>
					{{#if_shortAbstract}}
					{{shortAbstract}}{{#if_enWikiUrl}} <a href="{{enWikiUrl}}" class="newwindow">[more from Wikipedia]</a>{{/if_enWikiUrl}}
					{{/if_shortAbstract}}
					{{#if_links_without_shortAbstract}}
					Links:
					{{/if_links_without_shortAbstract}}
					{{#if_dbpediaUrl}}
					<br/><a href="{{dbpediaUrl}}" class="newwindow">DBPedia</a>
					{{/if_dbpediaUrl}}
					{{#if_VIAFLink}}
					{{#links}}
					<br/><a href="{{VIAFLink}}" class="newwindow">VIAF Record</a>
					{{/links}}
					{{/if_VIAFLink}}
					{{#if_BNFLink}}
					{{#links}}
					{{#BNFLink}}
					<br/><a href="{{.}}" class="newwindow">BNF Record</a>
					{{/BNFLink}}
					{{/links}}
					{{/if_BNFLink}}
					{{#if_DNBLink}}
					{{#links}}
					{{#DNBLink}}
					<br/><a href="{{.}}" class="newwindow">DNB Record</a>
					{{/DNBLink}}
					{{/links}}
					{{/if_DNBLink}}
					{{#if_worldCatIdUrl}}
					{{#links}}
					{{#worldCatIdUrl}}
					<br/><a href="{{.}}" class="newwindow">WorldCat Identities</a>
					{{/worldCatIdUrl}}
					{{/links}}
					{{/if_worldCatIdUrl}}
					{{#if_theatricaliaUrl}}
					{{#links}}
					{{#theatricaliaUrl}}
					<br/><a href="{{.}}" class="newwindow">Theatricalia</a>
					{{/theatricaliaUrl}}
					{{/links}}
					{{/if_theatricaliaUrl}}
					{{#if_imdbUrl}}
					{{#links}}
					{{#imdbUrl}}
					<br/><a href="{{.}}" class="newwindow">IMDb</a>
					{{/imdbUrl}}
					{{/links}}
					{{/if_imdbUrl}}
					{{#if_ibdbUrl}}
					{{#links}}
					{{#ibdbUrl}}
					<br/><a href="{{.}}" class="newwindow">IBDB</a>
					{{/ibdbUrl}}
					{{/links}}
					{{/if_ibdbUrl}}
					{{#if_sameAs}}
					{{#links}}
					{{#sameAs}}
					<br/><a href="{{.}}" class="newwindow">Other</a>
					{{/sameAs}}
					{{/links}}
					{{/if_sameAs}}
					<p>
				</div>
			</div>
			`,params);

		(callback1 ? callback1(output) : false);

		var id = params.id;

		$("#" + id + " .newwindow").click(function() {
			url = $(this).attr('href');
			window.open(url, '_blank');
			return false;
		});

		$('#' + id + ' h2').css('background-color', '#578cb5');
		$('#' + id + ' h2').css('background-image', 'none');
		$('#' + id + ' h2,#' + id + ' div').css('border-color', '#578cb5');
		$('#' + id + ' h2').css('color', 'white');
		$('#' + id + ' a').addClass('body_link_11');
/*		if (!params.first_box) {
			$('#' + id + ' .accordion_window').css('display','none');
		}*/
		$('.sidebar_accordion_header_icon_closed').css('background-image','url(/ui/cdm/default/collection/default/css/images/lightness-ui-icons_ffffff_256x240.png)');
		$('.sidebar_accordion_header_icon_open').css('background-image','url(/ui/cdm/default/collection/default/css/images/lightness-ui-icons_ffffff_256x240.png)');
		$('.ui-sidebar-icon-triangle-1-e').css('background-position','-35px -19px')
		$('.ui-sidebar-icon-triangle-1-s').css('background-position','-67px -19px')
		$('#verticalDragbarImg').css('visibility', 'hidden');
		(callback2 ? callback2(output) : false);
//        $('#verticalDragbarImg').css('visibility', 'hidden');
	}

	//Niko start coding for left side menu 
	$(document).ready(function() {
		//$('#image_title,#title_desc_bar').wrap('<div id="wrapper" style="overflow: auto"></div>');
		$('#image_title, #title_desc_bar, #tabs, #details').wrapAll('<div id="wrapper2"></div>');
		$('#wrapper2').wrap('<div id="wrapper"></div>');
		$('#wrapper').prepend('<div id="sidebar" style="width:25%; float:left;margin: 10px 5px;"></div>');
		$('#sidebar').prepend('<div id="side-title" style="margin: 0px 0px 10px"></div>');
		$('#sidebar').append('<div id="side-spacer" style="margin: 0px 5px 5px"></div>');
		$('#sidebar').append('<div id="side-play" style="margin: 0px 5px 10px"></div>');
		$('#sidebar').append('<div id="side-author" style="margin: 0px 5px 10px"></div>');
		$('#sidebar').append('<div id="side-coauthor" style="margin: 0px 5px 10px"></div>');
		$('#sidebar').append('<div id="side-theater" style="margin: 0px 5px 10px"></div>');
		$('#sidebar').append('<div id="side-motley-group" style="margin: 0px 5px 10px"></div>');
		//$('#side-title').html($('#image_title').html());
		$('#side-title').html('<h1 class="cdm_style">External Resources</h1>');
		if ($('#co-sidebar-wrapper').length > 0) {
			$('#wrapper').append($('#LeftPane'));
			$('#wrapper').append($('#co-sidebar-wrapper'));
			$('#leftPaneContent').append($('#wrapper2'));
			$('#leftPaneContent').prepend($('#image_title'));
		}
		//$('#verticalDragbarImg').hide();
		var locale = 'en';
		data = JSON.parse($("#rdf").html());
//        console.log(JSON.stringify(data));

		addLinks = function(target,otherUrls) {
			if (otherUrls !== undefined) {
				for (var j = 0; j < otherUrls.length; j++) {
					var otherUrl = otherUrls[j];
					if (otherUrl.includes('theatricalia.com')) {
						if (!otherUrl.includes('theatricalia.com/play/2/hamlet/production/mqd')) {
							target.links.theatricaliaUrl.push(otherUrl);
						}
					}
					else if (otherUrl.includes('worldcat.org/identities')) {
						target.links.worldCatIdUrl.push(otherUrl);
					}
					else if (otherUrl.includes('imdb.com')) {
						target.links.imdbUrl.push(otherUrl);
					}
					else if (otherUrl.includes('en.wikipedia.org') && target.enWikiUrl === undefined) {
						target.enWikiUrl = otherUrl;
					}
					else if (otherUrl.includes('viaf.org') && target.ViafUrl === undefined) {
						target.ViafUrl = otherUrl;
					}
					else {
						target.links.sameAs.push(otherUrl);
					}
				}
			}
		};

		var promises = []
		
		//playUrl = data['isPartOf'][1]['sameAs'];
		var perfObj = getObjectWithAttr(data['isPartOf'],'name');
		if (perfObj !== undefined) {
/*			var performanceObject = undefined
			if (perfObj['sameAs'] !== undefined) {
				performanceObject = perfObj['sameAs']
			}
			if (perfObj['@id'] !== undefined) {
				if (performanceObject !== undefined) {
					performanceObject.push(perfObj['@id'])
				} else {
					performanceObject = perfObj['@id']
				}
			}
			perfObj = performanceObject
		}
		
		if (perfObj !== undefined) {*/
			var playArr = [];
			if (Array.isArray(perfObj)) {
				for (j = 0; j < perfObj.length; j++) {
					var enWikiUrl = perfObj[j]['enWikiUrl']
					var ViafUrl = perfObj[j]['ViafUrl']
					if ( '@id' in perfObj[j]) {
						if (perfObj[j]['@id'].search('viaf.org') >= 0) {
							ViafUrl = perfObj[j]['@id']
						} else if (perfObj[j]['@id'].search('en.wikipedia.org') >= 0) {
							enWikiUrl = perfObj[j]['@id']
						}
					}

					var performance = new PerformanceEntity(j+1, perfObj[j]['@id'], perfObj[j]['homepage'], perfObj[j]['longAbstract'], perfObj[j]['shortAbstract'], perfObj[j]['name'], enWikiUrl, ViafUrl, perfObj[j]['dateCreated'], perfObj[j]['playSubject']);
					addLinks(performance,perfObj[j]['sameAs']);
					playArr.push(performance);
				}
			} else {
				var enWikiUrl = perfObj['enWikiUrl']
				var ViafUrl = perfObj['ViafUrl']
				if ( '@id' in perfObj) {
					if (perfObj['@id'].search('viaf.org') >= 0) {
						ViafUrl = perfObj['@id']
					} else if (perfObj['@id'].search('en.wikipedia.org') >= 0) {
						enWikiUrl = perfObj['@id']
					}
				}

				var performance = new PerformanceEntity(1, perfObj['@id'], perfObj['homepage'], perfObj['longAbstract'], perfObj['shortAbstract'], perfObj['name'], enWikiUrl, ViafUrl, perfObj['dateCreated'], perfObj['playSubject']);
				addLinks(performance,perfObj['sameAs']);
				playArr.push(performance);
			}
			
			//Render array into array of resources
			for (var i = 0; i < playArr.length; i++) {
				var performanceUrl = playArr[i]['identifier'];
				
				if (playArr[i]['enWikiUrl'] !== undefined || playArr[i]['ViafUrl'] !== undefined) {
					promises.push((function(i) {
						var dfd = $.Deferred();
						
						grabContentFromWeb(playArr[i]['enWikiUrl'],playArr[i]['ViafUrl'],function(result) {
							if (!result.error) {
								playArr[i].premiere = (result.wikiData.resource['http://dbpedia.org/property/premiere'] ? result.wikiData.resource['http://dbpedia.org/property/premiere'][0].value : false);
								playArr[i].playSubject = (result.wikiData.resource['http://dbpedia.org/ontology/subjectOfPlay'] ? result.wikiData.resource['http://dbpedia.org/ontology/subjectOfPlay'][0].value : false);
								playArr[i].homePage = (result.wikiData.resource['http://xmlns.com/foaf/0.1/homepage'] ? result.wikiData.resource['http://xmlns.com/foaf/0.1/homepage'][0].value : undefined);
								playArr[i].longAbstract = result.wikiData.longAbstract;
								playArr[i].shortAbstract = result.wikiData.shortAbstract;
								playArr[i].name = result.wikiData.title;
								playArr[i].dbpediaUrl = result.wikiData.dbpediaUrl;
								playArr[i].id = 'play-' + i;
								
								playArr[i].enWikiUrl = playArr[i].enWikiUrl || result.wikiUrl;
								playArr[i].ViafUrl = playArr[i].ViafUrl || result.viafUrl;

								if (playArr[i].name) {
									var info_box = new accordionObject(playArr[i].id,undefined,playArr[i].name,undefined,undefined,playArr[i].dbpediaUrl,undefined,playArr[i].enWikiUrl,undefined,playArr[i].homePage,playArr[i].ViafUrl,(playArr[i].links.BNFLinks.length > 0 ? playArr[i].links.BNFLinks : undefined),(playArr[i].links.DNBLinks.length > 0 ? playArr[i].links.DNBLinks : undefined),(playArr[i].links.worldCatIdUrl.length > 0 ? playArr[i].links.worldCatIdUrl : undefined),(playArr[i].links.theatricaliaUrl.length > 0 ? playArr[i].links.theatricaliaUrl : undefined),(playArr[i].links.imdbUrl.length > 0 ? playArr[i].links.imdbUrl : undefined),(playArr[i].links.ibdbUrl.length > 0 ? playArr[i].links.ibdbUrl : undefined),(playArr[i].links.sameAs.length > 0 ? playArr[i].links.sameAs : undefined),playArr[i].longAbstract,undefined,playArr[i].playSubject,playArr[i].premiere,undefined,playArr[i].shortAbstract)
									wrapWindow(info_box, function(absDialog) {
										$('#side-play').append(absDialog);
									});
								}
							}
							dfd.resolve();
						});
						return dfd.promise();
					})(i));
				}
			}
		}
		
		//get person
		var roles = {'author': { target_field: 'exampleOfWork', individuals: [] }, 'coauthor' : { target_field: 'contributor', individuals: [] }}
		var people = []
		for (var role in roles) {
			var personObj = getObjectWithAttr(data['isPartOf'],roles[role].target_field);
			if (personObj !== undefined) {
				if (role === 'author') {
					personObj = personObj['exampleOfWork']['author'];
				} else {
					personObj = personObj['contributor'];
				}
				
	//			var people = [];
				roles[role].individuals = people;
				if (Array.isArray(personObj)) {
					for (var i = 0; i < personObj.length; i++) {
						var enWikiUrl = personObj[i]['enWikiUrl']
						var ViafUrl = personObj[i]['ViafUrl']
						if ( '@id' in personObj[i]) {
							if (personObj[i]['@id'].search('viaf.org') >= 0) {
								ViafUrl = personObj[i]['@id']
							} else if (personObj[i]['@id'].search('en.wikipedia.org') >= 0) {
								enWikiUrl = personObj[i]['@id']
							}
						}
						var person = new PersonEntity(people.length+1, personObj[i]['@id'], personObj[i]['homePage'], personObj[i]['longAbstract'], personObj[i]['shortAbstract'], personObj[i]['name'], enWikiUrl, ViafUrl, (personObj[i]['jobTitle'] ? personObj[i]['jobTitle'] : 'Author'), personObj[i]['gender'], personObj[i]['birthDate'], personObj[i]['deathDate']);
						addLinks(person,personObj[i]['sameAs']);
						var duplicate = false;
						for (var j = 0; j < people.length; j++) {
							if (person['name'] == people[j]['name'] && person['enWikiUrl'] == people[j]['enWikiUrl'] && person['ViafUrl'] == people[j]['ViafUrl'] && !(people[j]['jobTitle'].includes(person['jobTitle']))) {
								duplicate = true;
								people[j]['jobTitle'] = people[j]['jobTitle'] + ', ' + person['jobTitle'];
							}
						}
						if (!duplicate) {
							people.push(person);
						}
					}
				} else {
					var enWikiUrl = personObj['enWikiUrl']
					var ViafUrl = personObj['ViafUrl']
					if ( '@id' in personObj) {
						if (personObj['@id'].search('viaf.org') >= 0) {
							ViafUrl = personObj['@id']
						} else if (personObj['@id'].search('en.wikipedia.org') >= 0) {
							enWikiUrl = personObj['@id']
						}
					}
					var person = new PersonEntity(people.length+1, personObj['@id'], personObj['homePage'], personObj['longAbstract'], personObj['shortAbstract'], personObj['name'], enWikiUrl, ViafUrl, (personObj['jobTitle'] ? personObj['jobTitle'] : 'Author'), personObj['gender'], personObj['birthDate'], personObj['deathDate']);
					addLinks(person,personObj['sameAs']);
					var duplicate = false;
					for (var j = 0; j < people.length; j++) {
						if (person['name'] == people[j]['name'] && person['enWikiUrl'] == people[j]['enWikiUrl'] && person['ViafUrl'] == people[j]['ViafUrl'] && !(people[j]['jobTitle'].includes(person['jobTitle']))) {
							duplicate = true;
							people[j]['jobTitle'] = people[j]['jobTitle'] + ', ' + person['jobTitle'];
						}
					}
					if (!duplicate) {
						people.push(person);
					}
				}
			}
		}

		(function(people) {
			for (var i = 0; i < people.length; i++ ) {
				var personUrl = people[i]['identifier'];
				if (people[i].jobTitle.indexOf(',') >= 0) {
					var job = people[i].jobTitle.substring(0,people[i].jobTitle.indexOf(',')).toLowerCase()
				} else {
					var job = people[i].jobTitle.toLowerCase()
				}
				people[i].id = job.replace(/ /g,'-') + '-' + i;
				
				if (people[i]['enWikiUrl'] !== undefined || people[i]['ViafUrl'] !== undefined) {
					promises.push((function(i) {
						var dfd = $.Deferred();
						
						grabContentFromWeb(people[i]['enWikiUrl'],people[i]['ViafUrl'],function(result) {
							if (!result.error) {
								people[i].name = people[i].name || (result.wikiData !== undefined ? result.wikiData.title || (result.viafData !== undefined ? result.viafData.Name : undefined) : (result.viafData !== undefined ? result.viafData.Name : undefined));
								people[i].gender = result.viafData !== undefined ? result.viafData['Gender'] || people[i].gender : people[i].gender;
								people[i].birthDate = result.viafData !== undefined ? result.viafData['BirthDate'] || people[i].birthDate : people[i].birthDate;
								people[i].deathDate = result.viafData !== undefined ? result.viafData['DeathDate'] || people[i].deathDate : people[i].deathDate;
								people[i].longAbstract = result.wikiData !== undefined ? result.wikiData.longAbstract || people[i].longAbstract : people[i].longAbstract;
								people[i].shortAbstract = result.wikiData !== undefined ? result.wikiData.shortAbstract || people[i].shortAbstract : people[i].shortAbstract;
								people[i].dbpediaUrl = result.wikiData !== undefined ? result.wikiData.dbpediaUrl || people[i].links.dbpediaUrl : people[i].links.dbpediaUrl;

/*								if ('wikiData' in result) {
									people[i].dbpediaUrl = result.wikiData.dbpediaUrl
								}*/
								
								if ( result.wikiUrl !== undefined && people[i].enWikiUrl !== undefined  && result.wikiUrl !== people[i].enWikiUrl ) {
									person.links.sameAs.push(people[i].enWikiUrl);
									people[i].enWikiUrl = result.wikiUrl;
								}
								
								people[i].enWikiUrl = people[i].enWikiUrl || result.wikiUrl
								people[i].ViafUrl = people[i].ViafUrl || result.viafUrl
								
								links_list = ['VIAFLink', 'DNBLinks', 'BNFLinks'];
								if ('viafData' in result) {
									for (var j = 0; j < links_list.length; j++) {
										render = result.viafData[links_list[j]];
										if (render) {
											if (Array.isArray(render)) {
												for (var k = 0; k < render.length; k++) {
													if ( render[k] !== undefined ) {
														people[i].links[links_list[j]].push(render[k]);
													}
												}
											} else {
												if (result.viafData[links_list[j]] !== undefined) {
													people[i].links[links_list[j]].push(result.viafData[links_list[j]])
												}
											}
										}
									}
								}
								
//								console.log(people[i])
								var info_box = new accordionObject(people[i].id,people[i].jobTitle,people[i].name,undefined,people[i].birthdate,people[i].dbpediaUrl,people[i].deathdate,people[i].enWikiUrl,people[i].gender,undefined,people[i].ViafUrl,(people[i].links.BNFLinks.length > 0 ? people[i].links.BNFLinks : undefined),(people[i].links.DNBLinks.length > 0 ? people[i].links.DNBLinks : undefined),(people[i].links.worldCatIdUrl.length > 0 ? people[i].links.worldCatIdUrl : undefined),(people[i].links.theatricaliaUrl.length > 0 ? people[i].links.theatricaliaUrl : undefined),(people[i].links.imdbUrl.length > 0 ? people[i].links.imdbUrl : undefined),(people[i].links.ibdbUrl.length > 0 ? people[i].links.ibdbUrl : undefined),(people[i].links.sameAs.length > 0 ? people[i].links.sameAs : undefined),people[i].longAbstract,undefined,undefined,undefined,undefined,people[i].shortAbstract);
//								console.log(info_box)
								wrapWindow(info_box, function(absDialog) {
									if (info_box.id.substring(0,info_box.id.indexOf('-')) == 'author') {
										$('#side-author').append(absDialog);
									}
									else {
										$('#side-coauthor').append(absDialog);
									}
								});
							}
							
							dfd.resolve();
						});
						return dfd.promise();
					})(i));
				} else {
					var info_box = new accordionObject(people[i].id,people[i].jobTitle,people[i].name,undefined,people[i].birthdate,people[i].dbpediaUrl,people[i].deathdate,people[i].enWikiUrl,people[i].gender,undefined,people[i].ViafUrl,(people[i].links.BNFLinks.length > 0 ? people[i].links.BNFLinks : undefined),(people[i].links.DNBLinks.length > 0 ? people[i].links.DNBLinks : undefined),(people[i].links.worldCatIdUrl.length > 0 ? people[i].links.worldCatIdUrl : undefined),(people[i].links.theatricaliaUrl.length > 0 ? people[i].links.theatricaliaUrl : undefined),(people[i].links.imdbUrl.length > 0 ? people[i].links.imdbUrl : undefined),(people[i].links.ibdbUrl.length > 0 ? people[i].links.ibdbUrl : undefined),(people[i].links.sameAs.length > 0 ? people[i].links.sameAs : undefined),people[i].longAbstract,undefined,undefined,undefined,undefined,people[i].shortAbstract);
					wrapWindow(info_box, function(absDialog) {
						if (info_box.id.substring(0,info_box.id.indexOf('-')) == 'author') {
							$('#side-author').append(absDialog);
						}
						else {
							$('#side-coauthor').append(absDialog);
						}
					});
				}
			}
		})(people);
		
		// get theather 
		var theaterObj = getObjectWithAttr(data['isPartOf'], 'locationCreated');
		if (theaterObj !== undefined) {
			theaterObj = theaterObj['locationCreated'];
			var theaters = [];
			if (Array.isArray(theaterObj)) {
				for (var i=0; i<theaterObj.length; i++) {
					var theater = new TheaterEntity(i+1, theaterObj[i]['@id'], theaterObj[i]['homePage'], theaterObj[i]['longAbstract'], theaterObj[i]['shortAbstract'], theaterObj[i]['name'], undefined, undefined, undefined, undefined);
					if (theater.identifier) {
						if (theater.identifier.search('en.wikipedia.org') >= 0) {
							theater.enWikiUrl = theater.identifier;
						} else if (theater.identifier.search('viaf.org') >= 0) {
							theater.ViafUrl = theater.identifier;
						}
					}
					addLinks(theater,theaterObj[i]['sameAs'])
					theaters.push(theater);                    
				}
			} else {
				var theater = new TheaterEntity(1, theaterObj['@id'], theaterObj['homePage'], theaterObj['longAbstract'], theaterObj['shortAbstract'], theaterObj['name'], undefined, undefined, undefined, undefined);
				if (theater.identifier) {
					if (theater.identifier.search('en.wikipedia.org') >= 0) {
						theater.enWikiUrl = theater.identifier;
					} else if (theater.identifier.search('viaf.org') >= 0) {
						theater.ViafUrl = theater.identifier;
					}
				}
				addLinks(theater,theaterObj['sameAs'])
				theaters.push(theater);
			}
			
			// TODO: need to account for possibility that no wikipedia url, but viaf or worldcat Ids instead...
			// TODO: need to update for putting other urls in links sub-hierarchy...
			for (var i = 0; i < theaters.length; i++) {
				var theaterUrl = theaters[i]['identifier'];                
				//console.log(theaterUrl);
				if (theaters[i]['enWikiUrl'] !== undefined || theaters[i]['ViafUrl'] !== undefined) {
					promises.push((function(i) {
						var dfd = $.Deferred();
						
						grabContentFromWeb(theaterUrl,undefined,function(result) {
							if (!result.error) {
								theaters[i].address =  result.wikiData !== undefined ? (result.wikiData.resource['http://dbpedia.org/ontology/address'] ? searchLiteral(result.wikiData.resource['http://dbpedia.org/ontology/address'], locale) : undefined) : undefined;
								theaters[i].seatingCapacity = result.wikiData !== undefined ? (result.wikiData.resource['http://dbpedia.org/ontology/seatingCapacity'] ? result.wikiData.resource['http://dbpedia.org/ontology/seatingCapacity'][0].value : undefined) : undefined;
								theaters[i].openingYear = result.wikiData !== undefined ? (result.wikiData.resource['http://dbpedia.org/ontology/openingYear'] ? result.wikiData.resource['http://dbpedia.org/ontology/openingYear'][0].value : undefined) : undefined;
								theaters[i].homePage = result.wikiData !== undefined ? (result.wikiData.resource['http://xmlns.com/foaf/0.1/homepage'] ? result.wikiData.resource['http://xmlns.com/foaf/0.1/homepage'][0].value : undefined) : undefined;
								theaters[i].longAbstract = result.wikiData !== undefined ? result.wikiData.longAbstract : theaters[i].longAbstract;
								theaters[i].shortAbstract = result.wikiData !== undefined ? result.wikiData.shortAbstract : theaters[i].shortAbstract;
								theaters[i].name = result.wikiData !== undefined ? result.wikiData.title : theaters[i].name;
								theaters[i].enWikiUrl = theaterUrl;
								theaters[i].dbpediaUrl = result.wikiData !== undefined ? result.wikiData.dbpediaUrl : undefined;
								
								var info_box = new accordionObject(theaters[i].id,undefined,theaters[i].name,theaters[i].address,undefined,theaters[i].dbpediaUrl,undefined,theaters[i].enWikiUrl,undefined,theaters[i].homePage,theaters[i].ViafUrl,(theaters[i].links.BNFLinks.length > 0 ? theaters[i].links.BNFLinks : undefined),(theaters[i].links.DNBLinks.length > 0 ? theaters[i].links.DNBLinks : undefined),(theaters[i].links.worldCatIdUrl.length > 0 ? theaters[i].links.worldCatIdUrl : undefined),(theaters[i].links.theatricaliaUrl.length > 0 ? theaters[i].links.theatricaliaUrl : undefined),(theaters[i].links.imdbUrl.length > 0 ? theaters[i].links.imdbUrl : undefined),(theaters[i].links.ibdbUrl.length > 0 ? theaters[i].links.ibdbUrl : undefined),(theaters[i].links.sameAs.length > 0 ? theaters[i].links.sameAs : undefined),theaters[i].longAbstract,theaters[i].openingYear,undefined,undefined,theaters[i].seatingCapacity,theaters[i].shortAbstract);
								wrapWindow(info_box, function(absDialog) {
									$('#side-theater').append(absDialog);
								});
							}
							dfd.resolve();
						});
						return dfd.promise();
					})(i));
				} else
				{
					var info_box = new accordionObject(theaters[i].id,undefined,theaters[i].name,theaters[i].address,undefined,theaters[i].dbpediaUrl,undefined,theaters[i].enWikiUrl,undefined,theaters[i].homePage,theaters[i].ViafUrl,(theaters[i].links.BNFLinks.length > 0 ? theaters[i].links.BNFLinks : undefined),(theaters[i].links.DNBLinks.length > 0 ? theaters[i].links.DNBLinks : undefined),(theaters[i].links.worldCatIdUrl.length > 0 ? theaters[i].links.worldCatIdUrl : undefined),(theaters[i].links.theatricaliaUrl.length > 0 ? theaters[i].links.theatricaliaUrl : undefined),(theaters[i].links.imdbUrl.length > 0 ? theaters[i].links.imdbUrl : undefined),(theaters[i].links.ibdbUrl.length > 0 ? theaters[i].links.ibdbUrl : undefined),(theaters[i].links.sameAs.length > 0 ? theaters[i].links.sameAs : undefined),theaters[i].longAbstract,theaters[i].openingYear,undefined,undefined,theaters[i].seatingCapacity,theaters[i].shortAbstract);
					wrapWindow(info_box, function(absDialog) {
						$('#side-theater').append(absDialog);
					});
				}
			}            
		}
		
/*		var creator = { 'identifier': data['creator']['@id'], 'name': data['creator']['name'], 'ViafUrl': data['creator']['@id'], 'enWikiUrl': data['creator']['sameAs'], 'type': data['creator']['@type'], 'links': { 'VIAFLink': [], 'BNFLinks': [], 'DNBLinks': [], 'worldCatIdUrl': [], 'theatricaliaUrl': [], 'imdbUrl': [], 'ibdbUrl': [], 'sameAs': [] } };
		promises.push((function(i) {
			var dfd = $.Deferred();
			grabContentFromWeb(creator.enWikiUrl,creator.ViafUrl,function(result) {
				if (!result.error) {
					creator.id = role + '-0';
					creator.name = creator.name || result.wikiData.title;
					creator.longAbstract = result.wikiData.longAbstract || creator.longAbstract;
					creator.shortAbstract = result.wikiData.shortAbstract || creator.shortAbstract;
					creator.dbpediaUrl = result.wikiData.dbpediaUrl;
					
					if ( result.wikiUrl !== undefined && creator.enWikiUrl !== undefined  && result.wikiUrl !== creator.enWikiUrl ) {
						person.links.sameAs.push(creator.enWikiUrl);
						creator.enWikiUrl = result.wikiUrl;
					}           
				}
				
				var info_box = new accordionObject(creator.id,undefined,creator.name,undefined,undefined,creator.dbpediaUrl,undefined,creator.enWikiUrl,undefined,undefined,creator.ViafUrl,undefined,undefined,undefined,undefined,undefined,undefined,undefined,creator.longAbstract,undefined,undefined,undefined,undefined,creator.shortAbstract)
				wrapWindow(info_box, function(absDialog) {
					$('#side-motley-group').append(absDialog);
				});
				
				dfd.resolve();
			});
			return dfd.promise();
		})(i));*/

		turnOnNewWindow = function(id) {
			$("#" + id + " a").click(function() {
				url = $(this).attr('href');
				window.open(url, '_blank');
				return false;
			});
		};

		turnOnNewWindow('metadata_play');
		turnOnNewWindow('metadata_theatr');
		turnOnNewWindow('metadata_creato');
		turnOnNewWindow('metadata_assocg');
		
		if ($('#co-sidebar-wrapper').length > 0) {
			$('#sidebar').css('width', '20%');
			$('#LeftPane').css('min-width', '250px');
			$('#LeftPane').css('width', '66%');
			$('#LeftPane').css('float', 'left');
			$('#LeftPane').css('position','relative');
			$('#image_title').css('padding-bottom','5px');
		}
		else {
			$('#wrapper2').css('min-width', '250px');
			$('#wrapper2').css('width', '70%');
			$('#wrapper2').css('float', 'left');
		}
		
		$('#sidebar').on('click', '.sidebar_accordion_header', function() {
			var target = $(this).next()
			if (target.is(':visible')) {
				target.hide();
				$(this).children().removeClass('sidebar_accordion_header_icon_open');
				$(this).children().removeClass('ui-sidebar-icon-triangle-1-s');
				$(this).children().addClass('sidebar_accordion_header_icon_closed');
				$(this).children().addClass('ui-sidebar-icon-triangle-1-e');
				$(this).children().css('background-position','-35px -19px');
			} else {
				target.show();
				$(this).children().removeClass('sidebar_accordion_header_icon_closed');
				$(this).children().removeClass('ui-sidebar-icon-triangle-1-e');
				$(this).children().addClass('sidebar_accordion_header_icon_open');
				$(this).children().addClass('ui-sidebar-icon-triangle-1-s');
				$(this).children().css('background-position','-67px -19px');
			}
		});
		
/*		$.when.apply($,promises).then(function() {
			var headers = $('.sidebar_accordion_header')
			headers[0].click()
		});*/
	});
}

window.addEventListener ? window.addEventListener('load',ready_function,false) : window.attachEvent && window.attachEvent('onload',ready_function);