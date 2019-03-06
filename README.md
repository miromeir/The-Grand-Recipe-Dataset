# The Grand Recipe Dataset

![visual_scheme](https://user-images.githubusercontent.com/7606509/53698452-8cc47080-3de5-11e9-8079-45f48ed58585.png)

## Abstract

This project seeks to learn facts about food habbits of different populations around the globe.

Food recipes are available everywhere - books, internet, etc = Lots of Data.

We achieve this - through Recipes!
For example:
> "Which ingredient is most widespread in Korea?"

> "Which country consumes the most sugar in their food?"
             
## The Data
Data can be obtained from many sources - cookbooks, websites, etc.
###### Representation:
In order to work with the data we decide on arbitrary XML-like format:

```
<recipe>
  <title>{Recipe Title}</title>
  <cuisine>{Origin Country/Area, e.g.: Indian / Thai / American / Chinese... </cuisine>
  <ingredients>
      <ingredient amount={e.g.; 2 Teaspoon, 1 Tablespoon, etc.} >{Ingredient}</ingredient>
      for example:
      <ingredient amount=3 Tablespoons> Tomato Sauce </ingredient>
      ...
      ...
      ...
  </ingredients>
</recipe>
```

## Crawler 
#### (See Folder: "Crawler")
Primary data achieved through web crawlers, on 2 major cooking websites.
Data was structured partially to the above scheme.
  Used:
- Python 3.5 + 
- Selenium driver
- PhantomJS
- Xpath Querys

## Tagging
#### (See "TagIngredients.py")

After aquiring raw data, it needs to be tagged to match the above structure.

Used:
- Python xml.etree Library
- SPARQL Query to Wikidata for list of possible ingredients.

> For each ingredient:
> 1. Measure it's **amount**compare against known measurment units, e.g. "3 tablespoons").
> 2. Determine main **ingredient_name** being used - (**See below How(*)**)
> 3. Write back to XML Tree as: ``` <ingredient amount={amount}> ingredient_name </ingredient> ```
###### (*) List of food ingredients was achieved via SPARQL Query from Wikidata:
```
  SELECT ?____ ?____Label WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
  { ?____ wdt:P31 wd:Q25403900. }
  UNION
  { ?____ wdt:P31 wd:Q1364. }
  UNION
  { ?____ wdt:P279 wd:Q2095. }
  UNION
  { ?____ wdt:P279 wd:Q3088299. }
  UNION
  { ?____ wdt:P31 wd:Q10675206. }
  UNION
  { ?____ wdt:P366 wd:Q10675206. }
  UNION
  { ?____ wdt:P279 wd:Q427457. }
  UNION
  { ?____ wdt:P279 wd:Q178359. }
  UNION
  { ?____ wdt:P279 wd:Q11004. }
  UNION
  { ?____ wdt:P279 wd:Q25403900. }
  UNION
  { ?____ wdt:P279 wd:Q1943539. }
  **r
  UNION
  { ?____ wdt:P279 wd:Q185217. }
  UNION
  { ?____ wdt:P279 wd:Q42962. }
  UNION
  { ?____ wdt:P279 wd:Q3314483. }
  UNION
  { ?____ wdt:P279 wd:Q283. }
  UNION
  {?____ wdt:P279 wd:Q10990.}
}
LIMIT 10000
```
**NOTE:** Extraction of food entities was considered first to be done with **N**amed **E**ntity **R**ecognition tools such as 
Spacy, But due to training difficulties a more naive approach was chosen.

Future versions will use NER for food recognition.

## Results:
- Overall, the crawlers scraped ~1870 recipes
- The tagger produced ~1555 relevant Recipes(relevant - which include a location).

**NOTE:** You are welcome to add more recipes of your own, as long as they follow the above structure guidelines.

## Adding Data / DTD Schemes
If you wish to add raw data to be tagged, please follow the following DTD scheme.

All **Untagged** Recipes must have the following header:
```
<?xml version = '1.0' ?>
<!DOCTYPE recipe [<!ELEMENT recipe ((title?,details?,ingredients, instructions?,cuisine) | (title?,cuisine,details?,ingredients, instructions?))>
<!ELEMENT title (#PCDATA)>
<!ELEMENT cuisine (#PCDATA)>
<!ELEMENT ingredients (#PCDATA)>
<!ELEMENT instructions (#PCDATA)>
<!ELEMENT details (#PCDATA)>
]>
```
All **Tagged** Recipes(with amount and ingredient identified) must have the following header:
```
<?xml version = "1.0" ?>

<!DOCTYPE recipe [
   <!ELEMENT recipe ((title?,details?,ingredients, instructions?,cuisine) | (title?,cuisine,details?,ingredients, instructions?))>
   <!ELEMENT title (#PCDATA)>
   <!ELEMENT cuisine (#PCDATA)>
   <!ELEMENT ingredients (ingredient*)>
   <!ELEMENT ingredient (#PCDATA)>
   <!ELEMENT instructions (#PCDATA)>
   <!ELEMENT details (#PCDATA)>
   <!ATTLIST ingredient amount CDATA #REQUIRED>
]>
```
## Usage Examples:
An example for a question we can answer will be:
##### "Which country consumes the most sugar in their food?"
Below are the average amounts of mg's of (granulated)sugar per recipe, for each tagged area in the world:
```
American:64.02849972497249
African:77.36111111111111
U.S.:76.64930555555556
Japanese:61.642943409247756
European:65.00735294117646
Latin American:56.04938271604939
Korean:46.387182454890784
Australian And New Zealander:52.773809523809526
Middle Eastern:64.23611111111111
Indian:0
Mexican:90.625
Chinese:58.17625661375661
Canadian:70.56712962962963
French:58.6082175925926
Thai:148.6193181818182
Mediterranean:16.25
Asian:102.875
Italian:43.125
Mediterranean:77.5
```

Asian and thai food are first, following U.S / American.
**Mediterranean** food seems to have the least granulated sugar in it.
