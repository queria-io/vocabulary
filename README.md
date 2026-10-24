# vocabulary

[日本語](README.ja.md)

A vocabulary that gives columns in Japanese open data shared names and meanings. Columns with different
names that refer to the same thing are tied together here. Queria is the first user, but this is not a
Queria-only spec: anyone, from national and local government to companies, can propose changes by pull request.

## Files

- `entities.csv`: what a column identifies (prefecture, municipality, grid square, corporation, ...).
  Columns that identify the same entity can be joined, even when their names or code formats differ
- `data_elements.csv`: what a column represents, and its standard name. These are data elements
  in the sense of ISO/IEC 11179
- `themes.csv`: what field a table's data belongs to. It follows the major statistical fields of e-Stat, the portal site
  for Japanese government statistics, and maps each to the EU Data Themes (`dcat:theme` in DCAT-AP)

For example, `prefecture_code` and `prefecture` (the name) are different data elements, but both identify
the `prefecture` entity.

## Columns of data_elements.csv

- `name`: the column name used in Japanese public data
- `title`: the Japanese label, from GIF, or IMI when GIF has none
- `schema_org`: the schema.org property
- `gif_class`, `gif_term`: the GIF class and English term. GIF URIs are provisional as of v2.4, so terms are referenced by the pair
- `imi_term`: the IMI core vocabulary term, under `http://imi.go.jp/ns/core/rdf#`
- `entity`: the entity this element identifies (a `name` in `entities.csv`), empty if it is not an identifier
- `type`, `format`: the type and the shape of values
- `aliases`: other column names for the same element, separated by `;`
- `note`: why a choice was made

## Naming

- General data (maps, places, data from outside Japan): schema.org terms in snake_case
- Japanese public data (national and local statistics and registers): GIF English terms in snake_case,
  except where the GIF term only qualifies a schema.org term (`latitudeOfRepresentativePoint`), in which case the shorter one wins
- Elements found in no vocabulary are added with the vocabulary columns left empty, and only when more than one dataset uses them

Existing abbreviations such as `lat` or `pref_code` go in `aliases`.

## Using it in a dataset

In a Queria dataset, a column in `*.table.yml` looks like this:

```yaml
- name: postal_code
  title: 郵便番号
  semantic: { role: entity, name: postal_code }
```

The column name follows `name` in `data_elements.csv` for Japanese public data, and the `schema_org` term in snake_case for general data (`name` when it is empty). `semantic.name` follows `name` in `entities.csv`. The full conventions are in [Dataset conventions](https://docs.queria.io/en/publish/conventions) on docs.queria.io.

A table's themes go in `dataset.yml` (for the whole dataset) or `*.table.yml` (per table) as `themes`, using `name`
from `themes.csv`. List as many as apply. A table without its own takes the dataset's.

```yaml
themes: [population]
```

## Columns of themes.csv

- `code`: the 2-digit code of the e-Stat statistical field (major category)
- `name`: the name written in `themes`
- `title`, `title_en`: labels. `title` is the e-Stat field name as is
- `eu_themes`: the matching EU Data Themes, separated by `;`. Used for data from outside Japan and for DCAT export
- `examples`, `examples_en`: examples of data in the theme, as a guide when unsure

## Sources

- schema.org: [schema.org](https://schema.org/) (CC BY-SA 3.0)
- GIF: [digital-go-jp/GIF](https://github.com/digital-go-jp/GIF) (Digital Agency)
- IMI: [Infrastructure for Multilayer Interoperability core vocabulary 2.4.2](https://imi.go.jp/core/core242/) (CC0 1.0)
- Statistical fields: [statistical fields of the e-Stat API](https://www.e-stat.go.jp/api/api-info/statsfield) (Statistics Bureau of Japan)
- EU Data Theme: [Data theme](http://publications.europa.eu/resource/authority/data-theme) (EU Publications Office)

These vocabularies are published on Queria as datasets (`schemaorg`, `gif`, `imi`) and can be queried with SQL.

## Checks

```bash
uv run scripts/check.py
```

Checks that entity names are unique, that every `entity` in `data_elements.csv` exists in `entities.csv`, that
the GIF and schema.org terms exist, that `name` is their snake_case form, that `aliases` do not collide, and that theme codes and names are unique with known EU Data Themes. CI runs it on every pull request.

## License

[CC0 1.0](LICENSE).
