function setFocus(graph,id,start_year,end_year,single_degree) {
	var output_graph = { 'nodes': [], 'links': [] };
	var degree_one = [];

	if (typeof single_degree == 'undefined') {
		single_degree = false;
	}
	var degree_two = [];

//Get target family/node
	for (var index = 0; index < graph['nodes'].length; index++) {
		if (graph['nodes'][index]['id'] == id) {
			var mention_sum = 0;
			for (y in graph['nodes'][index]['mention_count']) {
				if (y >= start_year && y <= end_year) {
					mention_sum += graph['nodes'][index]['mention_count'][y]
				}
			}
			var temp_obj = { 'mention_count': mention_sum, 'id': graph['nodes'][index]['id'], 'name': graph['nodes'][index]['name'] };
//			var temp_obj = { 'mention_count': graph['nodes'][index]['mention_count'], 'id': graph['nodes'][index]['id'], 'name': graph['nodes'][index]['name'] };
			temp_obj['group'] = 0;
			if (mention_sum > 0) {
				output_graph['nodes'].push(temp_obj);
			}
		}
	}

//Get links to first-degree connections
	for (var index = 0; index < graph['links'].length; index++) {
		if (graph['links'][index]['source'] == id || graph['links'][index]['target'] == id) {
			var value_sum = 0;
			for (y in graph['links'][index]['value']) {
				if (y >= start_year && y <= end_year) {
					value_sum += graph['links'][index]['value'][y]
				}
			}
			var temp_obj = { 'source': graph['links'][index]['source'], 'target': graph['links'][index]['target'], 'value': value_sum, 'name': graph['links'][index]['name'], 'degree': 1 };
//			var temp_obj = { 'source': graph['links'][index]['source'], 'target': graph['links'][index]['target'], 'value': graph['links'][index]['value'], 'name': graph['links'][index]['name'] };

			if (value_sum > 0) {
				output_graph['links'].push(temp_obj);
			}

			if (graph['links'][index]['source'] == id) {
				degree_one.push(graph['links'][index]['target']);
			}
			else {
				degree_one.push(graph['links'][index]['source']);
			}
		}
	}

//Get first-degree families/nodes
	for (var index = 0; index < graph['nodes'].length; index++) {
		if (degree_one.includes(graph['nodes'][index]['id'])) {
			var mention_sum = 0;
			for (y in graph['nodes'][index]['mention_count']) {
				if (y >= start_year && y <= end_year) {
					mention_sum += graph['nodes'][index]['mention_count'][y]
				}
			}
			var temp_obj = { 'mention_count': mention_sum, 'id': graph['nodes'][index]['id'], 'name': graph['nodes'][index]['name'] };
//			var temp_obj = { 'mention_count': graph['nodes'][index]['mention_count'], 'id': graph['nodes'][index]['id'], 'name': graph['nodes'][index]['name'] };
			temp_obj['group'] = 1;

			if (mention_sum > 0) {
				output_graph['nodes'].push(temp_obj);
			}
		}
	}

	if (single_degree) {
		//Get connections from first-degree families to other first-degree families
		for (var index = 0; index < graph['links'].length; index++) {
			if (degree_one.includes(graph['links'][index]['source']) && degree_one.includes(graph['links'][index]['target'])) {
				var value_sum = 0;
				for (y in graph['links'][index]['value']) {
					if (y >= start_year && y <= end_year) {
						value_sum += graph['links'][index]['value'][y]
					}
				}
				var temp_obj = { 'source': graph['links'][index]['source'], 'target': graph['links'][index]['target'], 'value': value_sum, 'name': graph['links'][index]['name'], 'degree': 2 };
	//			var temp_obj = { 'source': graph['links'][index]['source'], 'target': graph['links'][index]['target'], 'value': graph['links'][index]['value'], 'name': graph['links'][index]['name'] };

				if (value_sum > 0) {
					output_graph['links'].push(temp_obj);
				}
			}
		}

		return output_graph;
	}

//Get connections from first-degree families to second-degree families
	for (var index = 0; index < graph['links'].length; index++) {
		if (graph['links'][index]['source'] != id && graph['links'][index]['target'] != id && (degree_one.includes(graph['links'][index]['source']) || degree_one.includes(graph['links'][index]['target']))) {
			var value_sum = 0;
			for (y in graph['links'][index]['value']) {
				if (y >= start_year && y <= end_year) {
					value_sum += graph['links'][index]['value'][y]
				}
			}
			var temp_obj = { 'source': graph['links'][index]['source'], 'target': graph['links'][index]['target'], 'value': value_sum, 'name': graph['links'][index]['name'], 'degree': 2 };
//			var temp_obj = { 'source': graph['links'][index]['source'], 'target': graph['links'][index]['target'], 'value': graph['links'][index]['value'], 'name': graph['links'][index]['name'] };

			if (value_sum > 0) {
				output_graph['links'].push(temp_obj);
			}

			if (!degree_one.includes(graph['links'][index]['source'])) {
				degree_two.push(graph['links'][index]['source']);
			}
			else if (!degree_one.includes(graph['links'][index]['target'])) {
				degree_two.push(graph['links'][index]['target']);
			}
		}
	}

//Get second-degree families/nodes
	for (var index = 0; index < graph['nodes'].length; index++) {
		if (degree_two.includes(graph['nodes'][index]['id'])) {
			var mention_sum = 0;
			for (y in graph['nodes'][index]['mention_count']) {
				if (y >= start_year && y <= end_year) {
					mention_sum += graph['nodes'][index]['mention_count'][y]
				}
			}
			var temp_obj = { 'mention_count': mention_sum, 'id': graph['nodes'][index]['id'], 'name': graph['nodes'][index]['name'] };
//			var temp_obj = { 'mention_count': graph['nodes'][index]['mention_count'], 'id': graph['nodes'][index]['id'], 'name': graph['nodes'][index]['name'] };
			temp_obj['group'] = 2;
			output_graph['nodes'].push(temp_obj);
		}
	}

//Get links between second-degree families
	for (var index = 0; index < graph['links'].length; index++) {
		if (degree_two.includes(graph['links'][index]['source']) && degree_two.includes(graph['links'][index]['target'])) {
			var value_sum = 0;
			for (y in graph['links'][index]['value']) {
				if (y >= start_year && y <= end_year) {
					value_sum += graph['links'][index]['value'][y]
				}
			}
			var temp_obj = { 'source': graph['links'][index]['source'], 'target': graph['links'][index]['target'], 'value': value_sum, 'name': graph['links'][index]['name'], 'degree': 3 };
//			var temp_obj = { 'source': graph['links'][index]['source'], 'target': graph['links'][index]['target'], 'value': graph['links'][index]['value'], 'name': graph['links'][index]['name'] };

			if (value_sum > 0) {
				output_graph['links'].push(temp_obj);
			}
		}
	}

	return output_graph;
}

function removeID(graph,id) {
	nodes_to_remove = []
	ids_to_remove = []
	links_to_remove = []

	for (var index = 0; index < graph['nodes'].length; index++) {
		if (graph['nodes'][index]['id'] == id || graph['nodes'][index]['mention_count'] == 0) {
			nodes_to_remove.push(index);
			ids_to_remove.push(graph['nodes'][index]['id']);
		}
	}

	for (var i = nodes_to_remove.length-1; i >= 0; i--) {
		graph['nodes'].splice(nodes_to_remove[i],1);
	}

	for (var index = 0; index < graph['links'].length; index++) {
		if (ids_to_remove.includes(graph['links'][index]['source']) || ids_to_remove.includes(graph['links'][index]['target'])) {
			links_to_remove.push(index);
		}
	}

	for (var i = links_to_remove.length-1; i >= 0; i--) {
		graph['links'].splice(links_to_remove[i],1);
	}

	return graph
}