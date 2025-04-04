var addToCustomPortal = (function () {
	function getItem () {
		if (location.pathname.startsWith('/wiki/Q')) {
			return location.pathname.slice(6);
		}
	}

	function getProperty () {
		if (location.pathname.startsWith('/wiki/Property:P')) {
			return location.pathname.slice(15);
		}
	}

	function createLinkItem (id, label, url, description) {
		const li = document.createElement('li');
		li.setAttribute('id', id);
		li.setAttribute('class', 'mw-list-item');
		const a = document.createElement('a');
		a.setAttribute('href', url);
		a.setAttribute('title', description);
		a.innerText = label;
		li.append(a);
		return li;
	}

	function customPortal () {
		const sidePanel = document.getElementById('vector-page-tools');
		if(!sidePanel) return;
		const nav = document.createElement('div');
		nav.setAttribute('id', 'p-custom');
		nav.setAttribute('class', 'mw-portlet mw-portlet-tb vector-menu vector-menu-portal portal');
		nav.setAttribute('aria-labelledby', 'p-custom-label');
		nav.setAttribute('role', 'navigation');
		const label = document.createElement('div');
		label.setAttribute('id', 'p-custom-label');
		label.setAttribute('class', 'vector-menu-heading');
		label.innerHTML = '<span class="vector-menu-heading-label">Custom tools<span>';
		nav.append(label);
		const div = document.createElement('div');
		div.setAttribute('class', 'vector-menu-content');
		const ul = document.createElement('ul');
		ul.setAttribute('class', 'vector-menu-content-list');
		div.append(ul);
		nav.append(div);
		sidePanel.append(nav);
		return ul;
	}

	var list = customPortal();

	return function addToCustomPortal (callback) {
		const item = getItem();
		const property = getProperty();
		const links = callback(item, property);
		for (var i = 0; i < links.length; i++) {
			list.append(createLinkItem.apply(null, links[i]));
		}
	};
})();

addToCustomPortal(function (item, property) {
	var links = [];

	if (item) {
		links.push([
			't-custom-subclasses',
			'List subclasses',
			'https://query.wikidata.org/embed.html#SELECT%2aWHERE%7B%3Fo%20wdt%3AP279%20wd%3A' +
			item + '.%3Fo%20rdfs%3Alabel%20%3Fl.FILTER%28LANG%28%3Fl%29%3D%27en%27%29%7D',
			'List subclasses of an item'
		]);
		links.push([
			't-custom-instances',
			'List instances',
			'https://query.wikidata.org/embed.html#SELECT%2aWHERE%7B%3Fo%20wdt%3AP31%20wd%3A' +
			item + '.%3Fo%20rdfs%3Alabel%20%3Fl.FILTER%28LANG%28%3Fl%29%3D%27en%27%29%7DLIMIT%205000',
			'List 5000 instances of an item'
		]);
	} else if (property) {
		links.push([
			't-custom-subproperties',
			'List subproperties',
			'https://query.wikidata.org/embed.html#SELECT%2aWHERE%7B%3Fp%20wdt%3AP1647%20wd%3A' +
			property + '.%3Fp%20rdfs%3Alabel%20%3Fl.FILTER%28LANG%28%3Fl%29%3D%27en%27%29%7D',
			'List subproperties of a property'
		]);
	}

	return links;
});

addToCustomPortal(function (item, property) {
	if (item) {
		return [
			[
				't-custom-scholia',
				'Scholia page',
				'https://scholia.toolforge.org/' + item,
				'Go to the Scholia page of this item'
			]
		];
	} else {
		return [];
	}
});

addToCustomPortal(function (item, property) {
	var links = [];

	if (item) {
		links.push([
			't-custom-cite',
			'Cite',
			'https://citation-js.toolforge.org/export?id=' + item,
			'Cite this item'
		]);
	}

	return links;
});	


const query = `SELECT ?o ?oLabel WHERE {
			?o wdt:${property} [].
			SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
		} LIMIT 5000`
		
		
$a.attr('href', 'https://query.wikidata.org/embed.html#' + encodeURIComponent(query));







const query = `SELECT ?o ?oLabel WHERE {
?o wdt:${property}/^ps:${property} wds:${statement}.
SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }} LIMIT 5000	`
		
		
$a.attr('href', 'https://query.wikidata.org/embed.html#' + 
encodeURIComponent(query));