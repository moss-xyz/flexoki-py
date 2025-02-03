# flexoki-py

---

**Documentation**: See the rest of this readme, as well as the `docs` folder.

**Source Code**: [Available on GitHub](https://github.com/moss-xyz/flexoki-py)

---

### Introduction

*flexoki-py* is a Python library that provides easy access to [Flexoki](https://github.com/kepano/flexoki), an "inky color scheme for prose and code".

The intent behind this package is to make the colors from Flexoki accessible to other Python packages centered around graphics, especially [matplotlib](https://github.com/matplotlib/matplotlib).

Key features:

- Access to full library of Flexoki 2.0 colors
- Shortcuts to collections of colors (referred to as "Palettes")
- Robust filtering of colors based on hue and lightness
- Ability to register colors and palettes with matplotlib (as named colors and colormaps, respectively)

---

### Quick Start

#### Install and Import

*flexoki-py* can be installed via pip:

```bash
pip install flexoki-py
```

This package requires `python>=3.9.0` and `matplotlib>=3.9.0`, mainly because those are the two versions that I used in its development. It might work with older version, but no guarantees.

Once installed, the following import structure is recommended:

```py
from flexoki import Flexoki
```

This will import an instantiated variable (`Flexoki`) from which the colors and palettes can be access (via `Flexoki.colors` and `Flexoki.palettes`, respectively).

You may also choose to import the main class directly, like so:

```py
from flexoki import FlexokiSchema
...
your_variable = FlexokiSchema() # No arguments are taken
```

Doing so will allow you to create your own instances of the `FlexokiSchema` class, which can be useful if you want to name it something different or have different settings for each.

#### Concepts and Framework

This package relies on three custom classes/objects to function:

- `Color`: corresponds to a single color with a specified `hue` and `lightness`; also has properties for `name`, `hex` (code), and `rgb`. Currently, these are hardcoded based on the definitions from Flexoki 2.0, but could eventually be manipulated programmatically if I learn how to represent the OKLab colorspace in Python.

- `Palette`: corresponds to a collection of `Color` objects, with a specified `name` and `colors` (a list of `Color` objects). It also has properties for `hex` (a list of hex codes) and `rgb` (a list of RGB tuples). Usually, either a monochromatic array of colors (i.e. same hue at different lightness values) or a "monolightness" array (i.e. different hues at the same lightness value).

- `FlexokiSchema`: This is the main object that will be used to access the colors and palettes. It has *subclasses* for `colors` (to access `Color` objects; `FlexokiSchema.colors`) and `palettes` (to access `Palette` objects; `FlexokiSchema.palettes`), as well as a variety of other functions for helping splice and filter the colors as needed.

As a note, this package has, in many ways, been *over*-engineered, mainly because I was using this as a learning opportunity. Thus, several methods are available for accomplishing the *same* task.

#### Accessing Colors

Individual colors are primarily accessed in one of two ways: via dictionary-retrieval, or via attribute calling.

**Dictionary retrieval example**
```py
from flexoki import Flexoki
# Both of these work in the same way
Flexoki.colors["red-50"]
Flexoki["red-50"]
```

**Attribute calling example**
```py
from flexoki import Flexoki
# This method only works on the colors subclass
Flexoki.colors.red_50
```

Note the difference between the names: dictionary retrieval uses dashes (`-`), while the attribute calling must use underscores instead (`_`).

This will return a `Color` object, with its own attributes such as `hex` and `rgb`. Accessing these is possible like so:

```py
from flexoki import Flexoki
Flexoki.colors.red_50.hex
Flexoki.colors.red_50.rgb
```

For more information on the `Color` object, see the documentation in `docs/`

#### Accessing Palettes

Palettes (groups of colors) can only be accessed as attributes of the `palettes` subclass, like so:

```py
from flexoki import Flexoki
Flexoki.palettes.reds # will return all the red hues, ordered from lightest to darkest
Flexoki.palettes.l150 # will return all the hues that have a lightness value of 150 (these palettes always start with l followed by 2 or 3 numbers)
```

Similar to `Color` objects, `Palette` objects allow for easy accessing of the names, hex codes, and rgb values of the underlying colors. See the documentation in `docs/` for examples on how to do so.

#### Setting a Theme

For convenience, this package also allows you to pick a single "default" lightness value to use for all colors, so that lightness values do not have to be specified.

As an example, if you are exclusively working in hues with a lightness value of 150, then running this code...

```py
from flexoki import Flexoki
Flexoki.lightness(150)
```

... would allow you to get `red-150`, by using the shorthand `red` instead:

```py
Flexoki.colors.red # red-150
Flexoki.colors.purple # purple-150
Flexoki.palettes.defaults # all the colors at a lightness value of 150
```

See the documentation in `docs/` for more examples on how this works.

#### Filtering for Colors

While many palettes are pre-generated and bundled with the `FlexokiSchema`, the `filter()` function allows users to select subsets of hues and lightness values and generate palettes that best suit their needs.

```py
from flexoki import Flexoki
# Can also be accessed via Flexoki.colors.filter()
Flexoki.filter(h=["red","blue","green"], # only return reds, blues, and greens
               l=range(150,300), # only return colors with a lightness value between 150 and 300 (inclusive)
               order="h_l", # order the colors by hue, and then by lightness
               returns="palette") # return a Palette object
```

For more details on each of the accepted arguments, see the documentation in `docs/`.

#### Integration with `matplotlib`

**Colors**

Most `matplotlib` plotting functions will accept either hex codes or rgb(a) arrays as an argument for color; therefore, basic compatibility with matplotlib is achieved using the `hex` and `rgb` attributes of a `Color` object:

```py
import matplotlib.pyplot
import pandas
from flexoki import Flexoki
...
# Assuming a Pandas dataframe (df), and a matplotlib Figure (fig) and Axis (ax)
...
df.plot(ax=ax, color=Flexoki.colors.cyan_500.hex, ...)
```

This package also includes a function, `register_matplotlib()`, which adds each of the colors in the schema to `matplotlib`'s *named color directory*, allowing them to be used in the same way as the package's bundled colors.

```py
import matplotlib.pyplot
import pandas
from flexoki import Flexoki
# Registering the colors with matplotlib, using the prefix "flexoki"
Flexoki.register_matplotlib()
# Now these colors can be accessed via string
df.plot(ax=ax, color="flexoki:cyan-500", ...)
```

Additional options for limiting which colors are registered, and customizing the prefix, are available; see the `docs/` section for details.

**Palettes**

`Palette` objects, both the defaults and ones create by the user, can be turned into `colormaps` with the function `to_colormap()`, allowing them to be used anywhere a colormap would be used:

```py
from flexoki import Flexoki
Flexoki.reds.to_colormap(kind="smooth") # will make a LinearSegmentedColormap (smooth gradient between colors)
Flexoki.l700.to_colormap(kind="discrete") # will make a ListedColormap (discrete colors visible)
```

These colormaps can also be *named and registered* with the colormap repository of `matplotlib` as part of this function: see the `docs/` section for examples of usage. Note that `register_matplotlib()` (shown above), does *not* register palettes, only colors.

---

### Example Usage

---

### Roadmap

I expect the next *major* update to this package to occur only if/when the main Flexoki framework is updated. Otherwise, I might make small tweaks there and there based on my own use of this package, as well as feedback from other users (if any).

### License