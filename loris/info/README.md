# How Info Extraction Works

Image information falls into two categories:
 1. Boilerplate information
 2. Information that is about the server/service and based on the configuration
 3. Information that is per-image, based on its attributes (size, color) etc.

With this understood, Image information is collected from two classes:

### `loris.compliance.Compliance`

(The class is in `loris/compliance/__init__.py`). This class is based entirely on server's configuration, with one small exception: `extra_qualities()` needs to know whether the image is color or not so that it can include/exclude the `"color"` quality as appropriate. Some of the properties of this class (like `max_area`, etc.) are required for validating image requests. Compliance objects are also castable as a `str` and will return `levelN`, suitable for the `profile` property, and castable and comparable as an `int` to you can do, e.g., `if my_compliance > 1: ...` etc.

### `loris.info.abstract_extractor.AbstractExtractor` and its subclasses/implementations

These classes instantiate an Info instance in the `extract` method, and, leveraging data from the `Compliance` object as well as the information they extract from the image, populate an `Info` instance and return it.

## The `Info` class population and serialization

Both the Info class and the extractor classes have access to the applications's Compliance instance and are required by their constructors:

```python
Info(compliance: Compliance, http_identifier: str)

AbstractExtractor(compliance: Compliance, app_configs: dict)
```

For the most part, the compliance information is added to Info instances by the extractor (first in the abstract class and then in the subclass). It is worth noting, however, that the extractors also have access to the application config, which includes additional options and values (like maxArea, etc) that are outside of the IIIF compliance options.
