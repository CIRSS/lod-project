<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<?php
	function getRootNumber($item_id_number) {
		$first_seperator_index = strpos(substr($item_id_number,0,10),'-');
		if (!$first_seperator_index) {
			$first_seperator_index = strpos(substr($item_id_number,0,10),'_');
		}
		$root_id_number = substr($item_id_number,0,$first_seperator_index).substr($item_id_number,$first_seperator_index+1,3);
		return $root_id_number;
	}

	ini_set('auto_detect_line_endings',true);
	$item_id = $_GET["id"];
	$collection_name = htmlspecialchars($_GET["collection"]);

	if ($collection_name == 'motley-new') {
		$collection_title = "Motley Collection of Theatre and Costume Design (New)";
		$collection_url = "/cdm/landingpage/collection/motley-new";
		$collection_folder = 'motley';
		$items = fopen("MotleyTest-FromCDM-20Jun2017.csv","r");
		$page_url = "http://imagesearch-test1.library.illinois.edu/cdm/ref/collection/motley-new/id/" . $item_id;
	} else if ($collection_name == 'actors') {
		$collection_title = "Portraits of Actors, 1720-1920 ";
		$collection_url = "/cdm/landingpage/collection/actors";
		$collection_folder = 'actors';
		$items = fopen("PoANew.csv","r");
		$page_url = "http://imagesearch-test1.library.illinois.edu/cdm/ref/collection/actors/id/" . $item_id;
	} else if ($collection_name == 'motley') {
		$collection_title = "Motley Collection of Theatre and Costume Design";
		$collection_url = "/cdm/landingpage/collection/motley-new";
		$collection_folder = 'motley';
		$items = fopen("MotleyTest-FromCDM-20Jun2017.csv","r");
		$page_url = "http://imagesearch-test1.library.illinois.edu/cdm/ref/collection/motley/id/" . $item_id;
	}

	$i = 0;
	while (($line = fgetcsv($items)) !== false) {
		if ($collection_name == 'motley-new' || $collection_name == 'motley') {
			if ($line[38] == $item_id) {
				$image_title = $line[0];
				$jpg_url = substr($line[31],strpos($line[31],'.edu')+4);

				if (strpos($line[39],'.cpd')) {
					$object_type = 'compound';
				}
				else {
					$object_type = 'single';
				}

				if ($object_type == 'compound') {
					$item_id_number = $line[30];
					$root_id_number = getRootNumber($item_id_number);

					$second_items = fopen("MotleyTest-FromCDM-20Jun2017.csv","r");
					$jpg_urls = [];
					$component_objects = [];
					while ($new_line = fgetcsv($second_items)) {
						if (getRootNumber($new_line[30]) == $root_id_number && !strpos($new_line[39],'.cpd')) {
							array_push($jpg_urls,substr($new_line[31],strpos($new_line[31],'.edu')+4));
							$new_component_object = [];

							$new_component_object['image_title'] = $new_line[0];
							$new_component_object['performance_title'] = $new_line[1];
							$new_component_object['opening_performance_date'] = $new_line[2];
							$new_component_object['theater'] = $new_line[3];
							$new_component_object['author'] = $new_line[4];
							$new_component_object['composer'] = $new_line[5];
							$new_component_object['set_designer'] = $new_line[6];
							$new_component_object['translator'] = $new_line[7];
							$new_component_object['producer'] = $new_line[8];
							$new_component_object['conductor'] = $new_line[9];
							$new_component_object['choreographer'] = $new_line[10];
							$new_component_object['director'] = $new_line[11];
							$new_component_object['editor'] = $new_line[12];
							$new_component_object['actor'] = $new_line[13];
							$new_component_object['architect'] = $new_line[14];
							$new_component_object['associated_people'] = [$new_component_object['composer'],$new_component_object['set_designer'],$new_component_object['translator'],$new_component_object['producer'],$new_component_object['conductor'],$new_component_object['choreographer'],$new_component_object['director'],$new_component_object['editor'],$new_component_object['actor']];
							$new_component_object['associated_titles'] = ['Composer','Set Designer','Translator','Producer','Conductor','Choreographer','Director','Editor','Actor'];
							$new_component_object['object'] = $new_line[15];
							$new_component_object['type'] = $new_line[16];
							$new_component_object['materials'] = $new_line[17];
							$new_component_object['support'] = $new_line[18];
							$new_component_object['dimensions'] = $new_line[19];
							$new_component_object['description'] = $new_line[20];
							$new_component_object['inscription'] = $new_line[21];
							$new_component_object['style'] = $new_line[22];
							$new_component_object['notes'] = $new_line[23];
							$new_component_object['production_notes'] = $new_line[24];
							$new_component_object['basic_descriptors'] = [$new_component_object['object'],$new_component_object['type'],$new_component_object['materials'],$new_component_object['support,$dimensions'],$new_component_object['description'],$new_component_object['inscription'],$new_component_object['style'],$new_component_object['notes'],$new_component_object['production_notes']];
							$new_component_object['basic_descriptor_titles'] = ['Object','Type','Material/Techniques','Support','Dimensions','Description','Inscription','Style or Period','Notes','Production notes'];
							$new_component_object['basic_descritpor_ids'] = ['type','typea','materi','suppor','dimens','descri','inscri','style','scene','produc'];
							$new_component_object['subject1'] = $new_line[25];
							$new_component_object['subject2'] = $new_line[26];
							$new_component_object['subject3'] = $new_line[27];
							$new_component_object['subjects'] = [$new_component_object['subject1'],$new_component_object['subject2'],$new_component_object['subject3']];
							$new_component_object['subject_descriptors'] = ['subjec','subjea','subjeb'];
							$new_component_object['subject_titles'] = ['Subject I (AAT)','Subject II (TGMI)','Subject III (LCSH)'];
							$new_component_object['rights'] = $new_line[28];
							$new_component_object['physical_location'] = $new_line[29];
							$new_component_object['inventory_number'] = $new_line[30];
							$new_component_object['jpg_url'] = substr($new_line[31],strpos($new_line[31],'.edu')+4);
							$new_component_object['collect_title'] = $new_line[32];

							array_push($component_objects,$new_component_object);
						}
					}
				}
				else {
					$icon = '/motley/icon/icon'.substr($line[39],0,-3).'jpg';
				}

				$performance_title = $line[1];
				$opening_performance_date = $line[2];
				$theater = $line[3];
				$author = $line[4];
				$composer = $line[5];
				$set_designer = $line[6];
				$translator = $line[7];
				$producer = $line[8];
				$conductor = $line[9];
				$choreographer = $line[10];
				$director = $line[11];
				$editor = $line[12];
				$actor = $line[13];
				$architect = $line[14];
				$associated_people = [$composer,$set_designer,$translator,$producer,$conductor,$choreographer,$director,$editor,$actor];
				$associated_titles = ['Composer','Set Designer','Translator','Producer','Conductor','Choreographer','Director','Editor','Actor'];
				$object = $line[15];
				$type = $line[16];
				$materials = $line[17];
				$support = $line[18];
				$dimensions = $line[19];
				$description = $line[20];
				$inscription = $line[21];
				$style = $line[22];
				$notes = $line[23];
				$production_notes = $line[24];
				$basic_descriptors = [$object,$type,$materials,$support,$dimensions,$description,$inscription,$style,$notes,$production_notes];
				$basic_descriptor_titles = ['Object','Type','Material/Techniques','Support','Dimensions','Description','Inscription','Style or Period','Notes','Production notes'];
				$basic_descritpor_ids = ['type','typea','materi','suppor','dimens','descri','inscri','style','scene','produc'];
				$subject1 = $line[25];
				$subject2 = $line[26];
				$subject3 = $line[27];
				$subjects = [$subject1,$subject2,$subject3];
				$subject_descriptors = ['subjec','subjea','subjeb'];
				$subject_titles = ['Subject I (AAT)','Subject II (TGMI)','Subject III (LCSH)'];
				$rights = $line[28];
				$physical_location = $line[29];
				$inventory_number = $line[30];
				$collect_title = $line[32];
				$jsonld_file = '.'.str_replace('/','\\',substr($line[33],strpos($line[33],'.edu')+4));
			}
		} else if ($collection_name == 'actors') {
			if ($line[20] == $item_id) {
				$image_title = $line[1];
				$jpg_url = str_replace('image','jpg',$line[22]);
				$icon = str_replace('jpg/','jpg/icon',$jpg_url);

				$id_number = $line[0];
				$date = $line[2];
				$role = $line[3];
				$play = $line[4];
				$subject = $line[5];
				$subjects = [$subject];
				$subject_descriptors = ['subjec'];
				$subject_titles = ['Subject'];
				$type = $line[6];
				$dimensions = $line[7];
				$technique = $line[8];
				$description = $line[11];
				$basic_descriptors = [$type,$dimensions,$technique,$description];
				$basic_descriptor_titles = ['Type','Dimensions','Technique','Description'];
				$basic_descritpor_ids = ['type','dimens','techni','descra'];
				$creator = $line[9];
				$publisher = $line[10];
				$rights = $line[12];
				$physical_collection = $line[13];
				$repository = $line[14];
				$digita = $line[15];
				$jsonld_file = './jsonld/poa/'.$item_id.'.json';
			}
		}
		$i++;
	}

	$page_title = $image_title . " :: " . $collection_title;

	function prettyPrint($full_text) {
		$output = '';
		$new_text = str_replace('&lt;','',str_replace('&gt;','',$full_text));
		$instances = explode(";",$new_text);
		for ( $index = 0; $index < count($instances); $index++ ) {
			$divider = strpos($instances[$index],'http');
			if (htmlspecialchars($_GET["collection"]) == 'motley') {
				$output = $output.substr($instances[$index], 0, $divider-1).'<br>';
			}
			else if ($divider != FALSE) {
				$output = $output.'<a href="'.substr($instances[$index],$divider).'" target="_blank" class="body_link_11">'.substr($instances[$index], 0, $divider-1).'</a><br>';
			}
			else {
				$output = $output.$instances[$index].'<br>';
			}
		}

		$output = substr($output, 0, count($output)-3);

		return $output;
	}
?>

<html xmlns="http://www.w3.org/1999/xhtml"
	xmlns:og="http://ogp.me/ns#" class="no-js">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	
	<title><?php echo $page_title ?></title>

	<?php echo '<meta property="og:title" content="'.$page_title.'" />' ?>
	<?php echo '<meta property="og:image" content="'.$page_url.'" />' ?>   <link rel="shortcut icon" type="image/x-icon" href="/ui/custom/default/collection/default/images/favicon.ico?version=1398739428" />
	<?php echo '<link rel="canonical" href="'.$page_url.'" />' ?>

	<link type="text/css" href="/ui/custom/default/collection/default/css/main.css?version=1496177791" rel="stylesheet" />

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
	<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.20/jquery-ui.min.js"></script>

	<script type="text/javascript">
		(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
		(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
		m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
		})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

		ga('create', 'UA-71219941-3');
		ga('send', 'pageview');
	</script>

	<?php
		if (!is_null($jsonld_file)) {
			echo '<script id="rdf" type="application/ld+json">';
			echo file_get_contents($jsonld_file);
			echo '</script>';
		}
	?>
</head>
<body>
	<div itemscope itemtype="http://schema.org/Thing">
		<?php echo '<meta itemprop="name" content="'.$page_title.'" />' ?>
		<?php echo '<meta itemprop="image" content="http://imagesearch-test1.library.illinois.edu'.$icon.'" />' ?>
	</div>

<!-- HEADER -->
	<div id="headerWrapper" tabindex="1000">
		<p><span style="font-size: xx-large; color: #ffffff;"><strong><span style="letter-spacing: -1px; font-family: arial,helvetica,sans-serif; margin-left: 15px;">Linked Open Data Website</span></strong></span></p>
		<span class="clear"></span>
	</div>

<!--  NAV_TOP -->
	<div id="nav_top">
		<div id="nav_top_left">
			<ul class="nav">
				<li class="nav_li">
					<a tabindex="1001" id="nav_top_left_first_link" href="/cdm/"  >
						<div class="nav_top_left_text_container">Home</div>
					</a>
				</li>
				<li class="nav_li">
				<?php 
					if ($collection_name == 'motley-new') {
						$sitemap_name = 'motley';
					}
					else if ($collection_name == 'actors') {
						$sitemap_name = 'actors';
					}

					echo '<a tabindex="1002"  href="/browse_'.$sitemap_name.'.html"  >';
					echo '<div class="nav_top_left_text_container">Browse All</div>';
					echo '</a>';
				?>
				</li>				
			</ul>
		</div>
	</div>

<!-- SEARCH -->
	
<!-- BEGIN TOP CONTENT -->
	<div id="top_content">
		<script>
			var cdm_imgDivBg;
			var cdm_imageviewerbgcolor;
			var cdm_imageviewerbgImg;
			var cdm_thumbnailOpenOnLoad = true;
			var cdm_thumbnailBoxOverlayColor = "#FF0000";
			var cdm_thumbnailBox = {"height": 0, "width": 0, "bgcolor": "white", "overlayColor": cdm_thumbnailBoxOverlayColor};
			var cdm_initialzoom = "width"
			var cdm_initialzoomcustom = "";
			var cdm_scaleArray = new Array(5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,125,150,200);

			cdm_imgDivBg = "";
			cdm_imageviewerbgcolor = "#EBEBEB";
			cdm_imageviewerbgImg = "";
		</script>

		<div id="breadcrumb_top">
			<div id="breadcrumb_top_content">
				<a href="/cdm/" class="action_link_10" tabindex="15">Home</a>
				<img src="/ui/cdm/default/collection/default/css/images/double_arrow_e.png" alt="arrow" />
				<?php echo '<a href="'.$collection_url.'" class="action_link_10" tabindex="16"> '.$collection_title.'</a>' ?>
<!--				<a href="/cdm/landingpage/collection/motley-new" class="action_link_10" tabindex="16"> Motley Collection of Theatre and Costume Design (New)</a>-->
				<img src="/ui/cdm/default/collection/default/css/images/double_arrow_e.png" alt="arrow" />
				<a href="/hamlet_item_index.html"  class="action_link_10" tabindex="17">Hamlet</a>
				<?php echo '<img src="/ui/cdm/default/collection/default/css/images/double_arrow_e.png" alt="arrow" /> '.$image_title ?>
			</div>
		</div>

		<!-- ITEM_TITLE -->
		<div id="image_title">
			<?php echo '<h1 class="cdm_style">'.$image_title.'</h1>' ?>
		</div>

		<!-- ITEM_VIEWER -->
		<div id="tabs" class="tabs spaceMar30B" thistab="tabdiv">
			<span class="clear"></span>
			<div id="content_main">
				<div id="img_view_container">
					<script src="/openseadragon/openseadragon.min.js"></script>
					<?php
						if ($collection_name == 'actors') {
							echo '<script type="text/javascript">
								var viewer = OpenSeadragon({
									id: "openseadragon1",
									prefixUrl: "/openseadragon/images/",
									showNavigator: true,
									tileSources: [{
										"type": "image",
										"url": "http://imagesearch-test1.library.illinois.edu:8080/Cantaloupe-3.3.1/iiif/2/'.urlencode($jpg_url).'/full/full/0/default.jpg"
									}]
								});
							</script>
							<div id="openseadragon1" style="height: 600px; background-color: black;"></div>';
						}
						else {
							if ($object_type == 'compound') {
								$compound_viewer = '<script type="text/javascript">
									var viewer = OpenSeadragon({
										id: "openseadragon1",
										prefixUrl: "/openseadragon/images/",
										showNavigator: true,
										sequenceMode: true,
										tileSources: [';

								for ($jpg_index = 0; $jpg_index < count($jpg_urls); $jpg_index++) {
									$compound_viewer.='{
										"type": "image",
										"url": "http://imagesearch-test1.library.illinois.edu:8080/Cantaloupe-3.3.1/iiif/2/'.urlencode($jpg_urls[$jpg_index]).'/full/full/0/default.jpg"
									}';

									if ($jpg_index+1 < count($jpg_urls)) {
										$compound_viewer.=',';
									}
								}

								$compound_viewer.=']';

								if ($collection_name == 'motley') {
									$compound_viewer.=',
									homeFillsViewer: true';
								}

								$compound_viewer.='	});
								</script>
								<div id="openseadragon1" style="height: 600px; background-color: black;"></div>';

								echo $compound_viewer;
							}
							else {
								$viewer = '<script type="text/javascript">
									var viewer = OpenSeadragon({
										id: "openseadragon1",
										prefixUrl: "/openseadragon/images/",
										showNavigator: true,
										tileSources: [{
											"type": "image",
											"url": "http://imagesearch-test1.library.illinois.edu:8080/Cantaloupe-3.3.1/iiif/2/'.urlencode($jpg_url).'/full/full/0/default.jpg"
										}]';

								if ($collection_name == 'motley') {
									$viewer.=',
									homeFillsViewer: true,
									maxZoomLevel: 1,
									minZoomLevel: 0.1';
								}

								$viewer.='	});
								</script>
								<div id="openseadragon1" style="height: 600px; background-color: black;"></div>';

								echo $viewer;
							}
						}
					?>
				</div><!-- end #img_view_container  -->
				<span class="clear"></span>
			</div><!-- end contentmain-->
			<span class="clear"></span>
		</div><!-- end #tabs -->
		<span class="clear"></span>
		<a name="meta"></a>

		<?php
			function buildDescriptionAccordion($accordion_name,$accordion_number,$id_number,$image_title,$date,$role,$play,$performance_title,$opening_performance_date,$theater,$author,$associated_people,$associated_titles,$basic_descriptors,$basic_descritpor_ids,$basic_descriptor_titles,$subjects,$subject_descriptors,$subject_titles,$creator,$publisher,$rights,$physical_collection,$repository,$digita,$physical_location,$inventory_number,$jpg_url,$collect_title,$jsonld_file) {
				echo '<h2 id="details_accordion_description_link_'.$accordion_number.'"  class="accordion_header accordion_header_open">';
				echo '<span class="accordion_header_icon ui-icon ui-icon-triangle-1-s accordion_header_icon_open"></span>';
				echo '<a>'.$accordion_name.'</a></h2>';
				echo '<div class="accordion_window"><table>';

				if (!is_null($id_number) && $id_number != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_identi">ID Number</td><td class="description_col2" id="metadata_identi">'.$id_number.'</td></tr>';
				}
			
				echo '<tr><td class="description_col1" id="metadata_nickname_title">Image Title</td>';
				echo '<td class="description_col2" id="metadata_title">'.$image_title.'</td></tr>';
			
				if (!is_null($date) && $date != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_date">Date</td>';
					echo '<td class="description_col2" id="metadata_date">'.prettyPrint(htmlspecialchars($date)).'</td></tr>';
				}
			
			
				if (!is_null($role) && $role != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_role">Role</td>';
					echo '<td class="description_col2" id="metadata_role">'.prettyPrint(htmlspecialchars($role)).'</td></tr>';
				}
			
			
				if (!is_null($play) && $play != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_play">Play</td>';
					echo '<td class="description_col2" id="metadata_play">'.prettyPrint(htmlspecialchars($play)).'</td></tr>';
				}
			
			
				if (!is_null($performance_title) && $performance_title != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_play">Performance Title</td><td class="description_col2" id="metadata_play">'.prettyPrint(htmlspecialchars($performance_title)).'</td></tr>';
				}
			
			
				if (!is_null($opening_performance_date) && $opening_performance_date != '') {
					echo '<tr><td class="description_col1" id="metadata_object_nickname_year">Opening Performance Date</td><td class="description_col2" id="metadata_object_year">'.prettyPrint(htmlspecialchars($opening_performance_date)).'</td></tr>';
				}
			
			
				if (!is_null($theater) && $theater != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_theatr">Theater</td>';
					echo '<td class="description_col2" id="metadata_theatr">'.prettyPrint(htmlspecialchars($theater)).'</td></tr>';
				}
			
			
				if (!is_null($author) && $author != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_creato">Author</td>';
					echo '<td class="description_col2" id="metadata_creato">'.prettyPrint(htmlspecialchars($author)).'</td></tr>';
				}
			
			
				if (!is_null($associated_people)) {
					for ( $index = 0; $index < count($associated_people); $index++) {
						if ( $associated_people[$index] !== '' ) {
							echo '<tr><td class="description_col1" id="metadata_nickname_assoc'.chr(ord('a') + $index).'">Associated People ('.$associated_titles[$index].')</td>';
							echo '<td class="description_col2" id="metadata_assoc'.chr(ord('a') + $index).'">'.prettyPrint(htmlspecialchars($associated_people[$index])).'</td></tr>';
						}
					}
				}
			
			
				for ( $index = 0; $index < count($basic_descriptors); $index++ ) {
					if (!is_null($basic_descriptors[$index]) && $basic_descriptors[$index] != '') {
						echo '<tr><td class="description_col1" id="metadata_nickname_'.$basic_descritpor_ids[$index].'">'.$basic_descriptor_titles[$index].'</td>';
						echo '<td class="description_col2" id="metadata_'.$basic_descritpor_ids[$index].'">'.prettyPrint($basic_descriptors[$index]).'</td></tr>';
					}
				}
			
			
				for ( $index = 0; $index < 3; $index++ ) {
					if(!is_null($subjects[$index]) && $subjects[$index] != '') {
						echo '<tr><td class="description_col1" id="metadata_nickname_'.$subject_descriptors[$index].'">'.$subject_titles[$index].'</td>';
						echo '<td class="description_col2" id="metadata_'.$subject_descriptors[$index].'">'.prettyPrint(htmlspecialchars($subjects[$index])).'</td></tr>';
					}
				}
			
			
				if (!is_null($creator) && $creator != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_format">Creator</td>';
					echo '<td class="description_col2" id="metadata_format">'.prettyPrint(htmlspecialchars($creator)).'</td></tr>';
				}
			
			
				if (!is_null($publisher) && $publisher != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_publis">Publisher</td>';
					echo '<td class="description_col2" id="metadata_publis">'.prettyPrint(htmlspecialchars($publisher)).'</td></tr>';
				}
			
			
				if (!is_null($rights) && $rights != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_rights">Rights</td>';
					echo '<td class="description_col2" id="metadata_rights">'.htmlspecialchars($rights).'</td></tr>';
				}
			
			
				if (!is_null($physical_collection) && $physical_collection != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_reposi">Physical Collection</td>';
					echo '<td class="description_col2" id="metadata_reposi">'.htmlspecialchars($physical_collection).'</td></tr>';
				}
			
			
				if (!is_null($repository) && $repository != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_reposa">Repository</td>';
					echo '<td class="description_col2" id="metadata_reposa">'.htmlspecialchars($repository).'</td></tr>';
				}
			
			
				if (!is_null($digita) && $digita != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_digita">Collection</td>';
					echo '<td class="description_col2" id="metadata_digita">'.htmlspecialchars($digita).'</td></tr>';
				}
			
			
				if (!is_null($physical_location) && $physical_location != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_reposi">Physical Location</td>';
					echo '<td class="description_col2" id="metadata_reposi">'.htmlspecialchars($physical_location).'</td></tr>';
				}
			
			
				if (!is_null($inventory_number) && $inventory_number != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_invent">Inventory Number</td>';
					echo '<td class="description_col2" id="metadata_invent">'.htmlspecialchars($inventory_number).'</td></tr>';
				}
			
			
				if (!is_null($jpg_url) && $jpg_url != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_jpeg20">JPEG URL</td>';
					echo '<td class="description_col2" id="metadata_jpeg20"><a href="'.htmlspecialchars($jpg_url).'" target="_blank" class="body_link_11">http://imagesearch-test1.library.illinois.edu'.htmlspecialchars($jpg_url).'</a></td></tr>';
				}
			
			
				if (!is_null($collect_title) && $collect_title != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_collec">Collection Title</td>';
					echo '<td class="description_col2" id="metadata_collec">'.htmlspecialchars($collect_title).'</td></tr>';
				}
			
			
				if (!is_null($jsonld_file) && $jsonld_file != '') {
					echo '<tr><td class="description_col1" id="metadata_nickname_rdfa">RDF</td>';
					echo '<td class="description_col2" id="metadata_rdfa"><a href="'.substr(str_replace('\\','/',htmlspecialchars($jsonld_file)),1).'" target="_blank" class="body_link_11">http://imagesearch-test1.library.illinois.edu'.substr(str_replace('\\','/',htmlspecialchars($jsonld_file)),1).'</a></td></tr>';
				}

				echo '</table></div>';
			}
		?>

		<!-- META_DATA -->
		<div id="details" class="details_accordion">
			<div id="details_accordion" class="cdm_togglebox">
				<?php
					if ($object_type == 'compound') {
						buildDescriptionAccordion('Object Description',0,$id_number,$image_title,$date,$role,$play,$performance_title,$opening_performance_date,$theater,$author,$associated_people,$associated_titles,$basic_descriptors,$basic_descritpor_ids,$basic_descriptor_titles,$subjects,$subject_descriptors,$subject_titles,$creator,$publisher,$rights,$physical_collection,$repository,$digita,$physical_location,$inventory_number,$jpg_url,$collect_title,$jsonld_file);

						for ($descripton_counter = 0; $descripton_counter < count($component_objects); $descripton_counter++) {
							buildDescriptionAccordion('Description',1,$component_objects[$descripton_counter]['id_number'],$component_objects[$descripton_counter]['image_title'],$component_objects[$descripton_counter]['date'],$component_objects[$descripton_counter]['role'],$component_objects[$descripton_counter]['play'],$component_objects[$descripton_counter]['performance_title'],$component_objects[$descripton_counter]['opening_performance_date'],$component_objects[$descripton_counter]['theater'],$component_objects[$descripton_counter]['author'],$component_objects[$descripton_counter]['associated_people'],$component_objects[$descripton_counter]['associated_titles'],$component_objects[$descripton_counter]['basic_descriptors'],$component_objects[$descripton_counter]['basic_descritpor_ids'],$component_objects[$descripton_counter]['basic_descriptor_titles'],$component_objects[$descripton_counter]['subjects'],$component_objects[$descripton_counter]['subject_descriptors'],$component_objects[$descripton_counter]['subject_titles'],$component_objects[$descripton_counter]['creator'],$component_objects[$descripton_counter]['publisher'],$component_objects[$descripton_counter]['rights'],$component_objects[$descripton_counter]['physical_collection'],$component_objects[$descripton_counter]['repository'],$component_objects[$descripton_counter]['digita'],$component_objects[$descripton_counter]['physical_location'],$component_objects[$descripton_counter]['inventory_number'],$component_objects[$descripton_counter]['jpg_url'],$component_objects[$descripton_counter]['collect_title'],$component_objects[$descripton_counter]['jsonld_file']);
						}
					}
					else {
						buildDescriptionAccordion('Description',0,$id_number,$image_title,$date,$role,$play,$performance_title,$opening_performance_date,$theater,$author,$associated_people,$associated_titles,$basic_descriptors,$basic_descritpor_ids,$basic_descriptor_titles,$subjects,$subject_descriptors,$subject_titles,$creator,$publisher,$rights,$physical_collection,$repository,$digita,$physical_location,$inventory_number,$jpg_url,$collect_title,$jsonld_file);
					}
				?>

				<?php
					if ($collection_name == 'motley-new') {
						echo '<script src="/mustache.js-master/mustache.js"></script>';
						echo '<script src="/motley.js"></script>';
					} else if ($collection_name == 'actors') {
						echo '<script src="/mustache.js-master/mustache.js"></script>';
						echo '<script src="/poa.js"></script>';
					} else if ($collection_name == 'motley') {
						echo '<script src="/motleyOld.js"></script>';	
					}
				?>
				</div>
			</div>
		</div><!-- End accordion -->
		<script type="text/javascript">
			$("#details").on('click','.accordion_header', function() {
				if ($(this).hasClass('accordion_header_open')) {
					$(this).removeClass('accordion_header_open');
					$(this).addClass('accordion_header_closed');
					$(this).next().hide();
					$(this).children().first().removeClass('ui-icon-triangle-1-s');
					$(this).children().first().removeClass('accordion_header_icon_open');
					$(this).children().first().addClass('ui-icon-triangle-1-e');
					$(this).children().first().addClass('accordion_header_icon_closed');
				} else if ($(this).hasClass('accordion_header_closed')) {
					$(this).removeClass('accordion_header_closed');
					$(this).addClass('accordion_header_open');
					$(this).next().show();
					$(this).children().first().removeClass('ui-icon-triangle-1-e');
					$(this).children().first().removeClass('accordion_header_icon_closed');
					$(this).children().first().addClass('ui-icon-triangle-1-s');
					$(this).children().first().addClass('accordion_header_icon_open');
				}
			});
		</script>

		<!-- META_DATA -->
	</div>

	<!-- FOOTER -->
	<span class="clear"></span>
	<div id="cdmFooterWrapper" class="spaceMar20T">
		<div id="backToTopLink" class="float_left spaceMar20L">
			<a href="#top" class="action_link_10" data-analytics='{"category":"navigation","action":"click","label":"Back to top link"}'>Back to top</a>
		</div>
		<span class="clear"></span>
		<div id="nav_footer">
			<div id="nav_footer_left">
				<ul class="nav">
					<li class="nav_footer_li"><a href="/cdm/">Home</a></li>						  
				</ul>
			</div>
			<br /><br />
		</div>
	<span class="clear"></span>
	</div>
</body>