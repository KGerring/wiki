//Ex Musica userscript by Nikki - all the cool kids are using it
mw.loader.load("//www.wikidata.org/w/index.php?title=User:Nikki/ExMusica.js&action=raw&ctype=text/javascript");

//Lectrician discog + embeds script
mw.loader.load("//www.wikidata.org/w/index.php?title=User:Lectrician1/discographies3.js&action=raw&ctype=text/javascript");
mw.loader.load("//www.wikidata.org/w/index.php?title=User:Lectrician1/embeds.js&action=raw&ctype=text/javascript");

//Nikki Shortcuts
mw.loader.load("//www.wikidata.org/w/index.php?title=User:Nikki/KeyShortcuts.js&action=raw&ctype=text/javascript");

//Nikki Expand It! Collapse It!
mw.loader.load("//www.wikidata.org/w/index.php?title=User:Nikki/ExpandReferences.js&action=raw&ctype=text/javascript");

//Nikki safemode
//mw.util.addPortletLink("p-cactions", mw.Uri().extend({ "safemode": "1" }).toString(), "Reload in safe mode");
mw.loader.using( ["mediawiki.Uri"], function () {mw.util.addPortletLink("p-cactions", mw.Uri().extend({ "safemode": "1" }).toString(), "Reload in safe mode")}); 

//Show my Ps and Qs
mw.loader.load("//www.wikidata.org/w/index.php?title=User:Nikki/ShowIDs.js&action=raw&ctype=text/javascript");

//Most uses
//mw.loader.load("//www.wikidata.org/w/index.php?title=User:Ainali/common-properties.js&action=raw&ctype=text/javascript");

//Search External Identifiers
//mw.loader.load('//www.wikidata.org/w/index.php?title=User:Luca.favorido/lookup_test.js&action=raw&ctype=text/javascript');

// [[User:MichaelSchoenitzer/quickpresets.js]]
//mw.loader.load( '//www.wikidata.org/w/index.php?title=User:Moebeus/quickpresets_settings.js&action=raw&ctype=text/javascript' );
//mw.loader.load( '//www.wikidata.org/w/index.php?title=User:MichaelSchoenitzer/quickpresets.js&action=raw&ctype=text/javascript' );

// [[User:MichaelSchoenitzer/quickpresets_beta.js]]
mw.loader.using(['wikibase'], function() {

	$.getScript( 'https://www.wikidata.org/w/index.php?title=User:MichaelSchoenitzer/quickpresets_beta.js&action=raw&ctype=text/javascript', function() {
		var quickpresets = new wb.Quickpresets();
		quickpresets.init();
	});
});
importScript('User:MichaelSchoenitzer/quickpresetsconfigurator.js');

//Show entity labels in notifications
mw.loader.load("//www.wikidata.org/w/index.php?title=User:Zvpunry/WikibaseEcho.js&action=raw&ctype=text/javascript" ); 

// [[User:Lockal/EditSum.js]]
mw.loader.load("//www.wikidata.org/w/index.php?title=User:Lockal/EditSum.js&action=raw&ctype=text/javascript" ); 

// [[User:Matěj Suchánek/checkSitelinks.js]]
// Add indicators to sitelinks if they are disambiguations/redirects
mw.loader.load("//www.wikidata.org/w/index.php?title=User:Matěj_Suchánek/checkSitelinks.js&action=raw&ctype=text/javascript" );

 // https://www.wikidata.org/wiki/User:Yarl
 // Dragdrop from Wiki preview
mw.loader.load("//www.wikidata.org/w/index.php?title=User:Yarl/DragNDrop.js&action=raw&ctype=text/javascript" );

// [[User:Magnus Manske/duplicate item.js]]
/*
This script can duplicate the current item, minus sitelinks and descriptions (not allowed by Wikidata). This will add a new link "Duplicate this item" to your toolbox sidebar.
Clicking will duplicate the item, and open it in a new tab/window, or alert you to an error.*/
mw.loader.load("//www.wikidata.org/w/index.php?title=User:Magnus_Manske/duplicate_item.js&action=raw&ctype=text/javascript" );

//IdentifierInput script///////////////////////////////////////
//<nowiki>
mw.loader.load("//www.wikidata.org/w/index.php?title=User:1Veertje/identifierInput.js&action=raw&ctype=text/javascript" );
//</nowiki>
//End IdentifierInput script///////////////////////////////////////

/* Add tab indexes */
mw.hook('wikibase.entityPage.entityView.rendered').add(function () {
	function maketabbable () {
		$(".wikibase-toolbar-button a:not([tabindex])").each(function () {
			this.tabIndex = 0;

			$(this).on("click keydown", function (event) {
				if (event.type === "click" || event.key == "Enter") {
					setTimeout(maketabbable, 500);
				}
			});
		});
	}
	maketabbable();
	mw.hook("wikibase.statement.saved").add(maketabbable);
});

//Lexeme tools
// [[User:Jon Harald Søby/ordbokIframe.js]]
mw.loader.load( "//www.wikidata.org/w/index.php?title=User:Jon_Harald_Søby/ordbokIframe.js&action=raw&ctype=text/javascript" );
// [[User:Jon Harald Søby/bøyningsklasse.js]]
mw.loader.load( "//www.wikidata.org/w/index.php?title=User:Jon_Harald_Søby/bøyningsklasse.js&action=raw&ctype=text/javascript" );
// [[User:Nikki/LexemeEntitySuggester.js]]
// mw.loader.load( "//www.wikidata.org/w/index.php?title=User:Nikki/LexemeEntitySuggester.js&action=raw&ctype=text/javascript" );
// [[User:Nikki/LexemeAddIPA.js]]
// addipa_p5237 = { "Q25167": "Q6457972" };
// addipa_alwaysshown = true;
// mw.loader.load("//www.wikidata.org/w/index.php?title=User:Nikki/LexemeAddIPA.js&action=raw&ctype=text/javascript");
// [[User:Nikki/LexemeInterwikiLinks.js]]
mw.loader.load("//www.wikidata.org/w/index.php?title=User:Nikki/LexemeInterwikiLinks.js&action=raw&ctype=text/javascript");
// [[User:Mahir256/syndepgraph.js]]
mw.loader.load("//www.wikidata.org/w/index.php?title=User:Mahir256/syndepgraph.js&action=raw&ctype=text/javascript");
//New toys
//importScript('User:Bargioni/WikiBridge.js');

//https://www.wikidata.org/wiki/User:Bargioni/UseAsRef
//importScript( 'User:Bargioni/UseAsRef.js' );
//mw.loader.load("//www.wikidata.org/wiki/User:Bargioni/UseAsRef.js&action=raw&ctype=text/javascript");
//mw.loader.load('//www.wikidata.org/w/index.php?title=User:Bargioni/UseAsRef.js&action=raw&ctype=text/javascript'); // [[User:Bargioni/UseAsRef.js]]

//Paste identifiers
//mw.loader.load("//www.wikidata.org/w/index.php?title=User:Nikki/AutoIdentifierInput.js&action=raw&ctype=text/javascript");

 // [[User:Eflyjason/Gadget-CreateNewItem.js]]
//mw.loader.load( '//www.wikidata.org/w/index.php?title=User:Eflyjason/Gadget-CreateNewItem.js&action=raw&ctype=text/javascript' );

/* Shape Ex */
// importScript('User:Teester/CheckShex.js');

// wd_useful fix
// var wd_useful_toolbar = true ;


//The Blame Game///////////////////////////////////////
//importScript("User:Ricordisamoa/WikidataTrust.js");

//Premed is the GOAT ////
//importScript('User:Premeditated/moedata.js' );

//Wikidata Item Quality
//importScript('User:Premeditated/wikidata-quality.js');


// importScript( 'User:Pasleim/derivedstatements.js' );  // [[User:Pasleim/derivedstatements.js]]

/* mw.loader.load( '//www.wikidata.org/w/index.php?title=User:Pasleim/derivedstatements.js&action=raw&ctype=text/javascript' ); */ // [[User:Pasleim/derivedstatements.js]]

// mw.loader.load( '//www.wikidata.org/w/index.php?title=User:Magnus_Manske/wikidata_useful.js&action=raw&ctype=text/javascript' ); // [[User:Magnus Manske/wikidata_useful.js]]

// [[m:User:Jon Harald Søby/diffedit.js]]
//mw.loader.load( '//meta.wikimedia.org/w/index.php?title=User:Jon_Harald_Søby/diffedit.js&action=raw&ctype=text/javascript' );

//Statement order ////
//mw.loader.load( '//www.wikidata.org/w/index.php?title=User:Tohaomg/rearrange values.js&action=raw&ctype=text/javascript' );