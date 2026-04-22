
Based on the Help:Searching guide, search parameters act as powerful filters to narrow your results beyond simple keyword matching.
Here is a summary of the primary parameters available:
 * **intitle:** Restricts results to pages where the query appears in the title. You can also use regex here, such as intitle:/regexp/.
 * **insource:** Used to find specific wikitext, including template arguments, URLs, and hidden HTML. This is the primary parameter for regular expression searches.
 * **incategory:** Filters results to pages assigned to a specific category. Note that it does not automatically include subcategories unless you use **deepcategory:**.
 * **prefix:** Matches only the beginning characters of a page name. This must be the **last** part of your search string.
 * **linksto:** Finds pages that contain an internal link to the specified article.
 * **hastemplate:** Locates pages that transclude a specific template, including meta-templates not visible in the local wikitext.
 * **subpageof:** Limits the search to subpages of a specified page, which is particularly useful in the "Wikipedia" or "User" namespaces.
 * articletopic: Uses machine learning to filter by broad subjects like "books" or "physics," and weights those results higher.
 * inproject: Limits results to pages associated with specific WikiProjects.
Are you interested in seeing how to combine these parameters to create a complex custom filter?
