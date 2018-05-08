# Repository for "Exploring the Benefits for Users of Linked Open Data for Digitized Special Collections"

- [Project Home Page](http://publish.illinois.edu/linkedspcollections/)

### Subfolders:

- **kolb-proust**: includes XSLT and Python scripts for enriching cards (TEI-XML), displaying cards in [XTF](https://xtf.cdlib.org/), and adding links to references that have been digitized; also includes scripts for creating and displaying json of family name co-occurence tables as graphs in browser (using [D3 js library](https://d3js.org/) and [D3-Annotation js library](http://d3-annotation.susielu.com/)).
- **linked-sp-mockups**: early mockups of interface designs that make use of links to name, performance, and theater entities.
- **simple-name-reconciliation**: link to folder in @dkudeki's repository that queries [VIAF Auto Suggest API](https://platform.worldcat.org/api-explorer/apis/VIAF/AuthorityCluster/AutoSuggest) to find VIAF links for personal and corporate names. 
- **theater-collections**: includes backend Python scripts for transforming CSV metadata files that have been enriched with links to JSON-LD ([schema.org](https://schema.org/) semantics) and JSON suitable for ingesting into Solr; also includes frontend (client-side) .js files used by browser to dynamically retrieve text, links and other information using links included in JSON-LD metadata. 
