
// Custom upper-right links
$.when( mw.loader.using('mediawiki.util'), $.ready ).then( function() {
    mw.util.addPortletLink( 'p-personal', '/wiki/User:Swpb/Useful_properties', 'Properties', 'pt-props', 'Useful properties', 'p', '#pt-userpage');
    mw.util.addPortletLink( 'p-personal', '/wiki/User:Swpb/Basic_concepts', 'Concepts', 'pt-cons', 'Basic concepts', 'c', '#pt-userpage');
    mw.util.addPortletLink( 'p-personal', 'https://quickstatements.toolforge.org/#/', 'QuickStatements!', 'pt-qs', 'QuickStatements', 'c', '#pt-userpage');
    mw.util.addPortletLink( 'p-personal', 'https://query.wikidata.org/#%23%20Title%0ASELECT%20%3Fitem%20%3FitemLabel%0AWHERE%0A%7B%0A%20%20%3Fitem%20wdt%3AP31%20wd%3AQ146.%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%20%23%20Helps%20get%20the%20label%20in%20your%20language%2C%20if%20not%2C%20then%20en%20language%0A%7D', 'SPARQL', 'pt-sparql', 'Sparql', 's', '#pt-userpage');
    mw.util.addPortletLink( 'p-personal', '/wiki/User:Swpb/Useful_properties', 'Properties', 'pt-props', 'Useful properties', 'p', '#pt-userpage');
    mw.util.addPortletLink( 'p-personal', '/wiki/Wikidata:WikiProject Deprecate P642/Use cases', 'P642', 'pt-of', 'P642 deprecation', '6', '#pt-userpage');
    mw.util.addPortletLink( 'p-personal', 'https://en.wikipedia.org/wiki/User:Swpb/query-generator', 'P642q', 'pt-ofq', 'P642 query generator', 'q', '#pt-userpage');
//    mw.util.addPortletLink( 'p-personal', '/wiki/User:Swpb/home/sub1', 'DEL', 'pt-del', 'Deletion tracking', 'd', '#pt-sandbox');
} );

//Enable re-arranging order of values of statements
importScript('User:Tohaomg/rearrange values.js');

//Classification - tool to spot and fix weird membership trees
importScript('User:TomT0m/classification.js');

//Add slider to prompt for an edit summary
mw.loader.load( '//www.wikidata.org/w/index.php?title=User:Lockal/EditSum.js&action=raw&ctype=text/javascript' ); // [[User:Lockal/EditSum.js]]

//Add button to automatically fill citation details from URL
mw.loader.load( '//www.wikidata.org/w/index.php?title=User:Aude/CiteTool.js&action=raw&ctype=text/javascript' ); // [[User:Aude/CiteTool.js]]

//Script to warn about conflicting superclasses on instance/subclass statements
mw.loader.load('//www.wikidata.org/w/index.php?title=User:JesseW/conflicting_superclass_warnings.js&action=raw&ctype=text/javascript'); // [[User:JesseW/conflicting_superclass_warnings.js]]

//Duplicate item
importScript( 'User:Magnus_Manske/duplicate_item.js' );