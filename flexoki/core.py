from typing import List, Optional, Tuple, Literal, Iterable
from dataclasses import dataclass
import matplotlib
import matplotlib.colors
import matplotlib.cm
from flexoki.utils import h_codes, l_values

### Color ###
# Class for each individual color in the palette
@dataclass
class Color:
    name: str
    h: str
    l: int
    hex: str
    rgb: Tuple[int, int, int]

    def __str__(self):
        return f"{self.name} ({self.hex})"
    
    @property
    def hue(self):
        return self.h
    
    @property
    def lightness(self):
        return self.l
    
    # Allowing each of the RGB elements to be callable
    @property
    def rgba(self):
        return (self.rgb[0], self.rgb[1], self.rgb[2], 1)
    
    @property
    def r(self):
        return self.rgb[0]
    
    @property
    def red(self):
        return self.rgb[0]
    
    @property
    def g(self):
        return self.rgb[1]
    
    @property
    def green(self):
        return self.rgb[1]
    
    @property
    def b(self):
        return self.rgb[2]
    
    @property
    def blue(self):
        return self.rgb[2]

### Palette ###
# Class for a list/collection of colors, with several helpers for modifying/extending the palette
class Palette:
    def __init__(self, colors=List[Color]):
        # All the colors that make up the palette will be stored in a list
        self.colors = colors
    
    # Function for returning the name
    def names(self):
        return [c.name for c in self.colors]
    
    # Function for accessing the hex and rgb(a) values
    # If names=True is passed to the function, will return a dict with names as key and hex/rgb(a) as values
    def hex(self, names: bool=False):
        if names == True:
            return {c.name:c.hex for c in self.colors}
        else:
            return [c.hex for c in self.colors]
    
    def rgb(self, names: bool=False):
        if names == True:
            return {c.name:c.rgb for c in self.colors}
        else:
            return [c.rgb for c in self.colors]

    def rgba(self, names: bool=False):
        if names == True:
            return {c.name:c.rgba for c in self.colors}
        else:
            return [c.rgba for c in self.colors]
    
    # Function for reversing the order of colors if needed
    def reverse(self):
        self.colors = self.colors[::-1]
        return self

    # Function to create a matplotlib colormap from the selected palette
    # If kind is set to 'discrete', will create a Listed Colormap
    # If kind is set to 'smooth', will create a LinearSegmentedColormap
    # If register is a string, that will be used to register it with matplotlib's colormaps list
    def to_colormap(self, kind: Literal["discrete", "smooth"]="discrete", register=None):
        if not isinstance(kind, str):
            raise Exception(f"Invalid input for kind: {kind}; the only accepted values are 'discrete' (for ListedColormaps) or 'smooth' (for LinearSegmentedColormaps).")
        elif kind.lower() not in ["discrete", "smooth"]:
            raise Exception(f"Invalid input for kind: {kind}; the only accepted values are 'discrete' (for ListedColormaps) or 'smooth' (for LinearSegmentedColormaps).")
        else:
            if kind == "discrete":
                cmap = matplotlib.colors.ListedColormap(self.hex())
            else:
                cmap = matplotlib.colors.LinearSegmentedColormap.from_list("mycmap", self.hex())
                matplotlib.cm.unregister("mycmap") # unregistering this specific colormap

            if register is not None and not isinstance(register, str):
                raise Exception(f"Invalid input for register: {register}; only strings are accepted.")
            else:
                matplotlib.colormaps.register(cmap, name=register)
            
            return cmap
        
### FlexokiSchema ###
# Class to store all the colors and allow for easy selection
class FlexokiSchema:
    def __init__(self):

        # Setting up default properties
        self._theme = "light"
        self._lightness = 400

        # This class will handle all the individual colors
        class colors:
            # Loading all colors on initialization
            def __init__(self):
                # Each color will be accessible from within this dictionary (FlexokiSchema.colors.dict)
                self.dict = {
                    # Base (and paper/black)
                    "paper"    :{"h":"k", "l":0,    "hex":"#FFFCF0", "rgb":(255, 252, 240)},
                    "base-0"   :{"h":"k", "l":0,    "hex":"#FFFCF0", "rgb":(255, 252, 240)}, # equivalent to paper
                    "base-50"  :{"h":"k", "l":50,   "hex":"#F2F0E5", "rgb":(242, 240, 229)},
                    "base-100" :{"h":"k", "l":100,  "hex":"#E6E4D9", "rgb":(230, 228, 217)},
                    "base-150" :{"h":"k", "l":150,  "hex":"#DAD8CE", "rgb":(218, 216, 206)},
                    "base-200" :{"h":"k", "l":200,  "hex":"#CECDC3", "rgb":(206, 205, 195)},
                    "base-300" :{"h":"k", "l":300,  "hex":"#B7B5AC", "rgb":(183, 181, 172)},
                    "base-400" :{"h":"k", "l":400,  "hex":"#9F9D96", "rgb":(159, 157, 150)},
                    "base-500" :{"h":"k", "l":500,  "hex":"#878580", "rgb":(135, 133, 128)},
                    "base-600" :{"h":"k", "l":600,  "hex":"#6F6E69", "rgb":(111, 110, 105)},
                    "base-700" :{"h":"k", "l":700,  "hex":"#575653", "rgb":( 87,  86,  83)},
                    "base-800" :{"h":"k", "l":800,  "hex":"#403E3C", "rgb":( 64,  62,  60)},
                    "base-850" :{"h":"k", "l":850,  "hex":"#343331", "rgb":( 52,  51,  49)},
                    "base-900" :{"h":"k", "l":900,  "hex":"#282726", "rgb":( 40,  39,  38)},
                    "base-950" :{"h":"k", "l":950,  "hex":"#1C1B1A", "rgb":( 28,  27,  26)},
                    "base-1000":{"h":"k", "l":1000, "hex":"#100F0F", "rgb":( 16,  15,  15)}, # equivalent to black
                    "black"    :{"h":"k", "l":1000, "hex":"#100F0F", "rgb":( 16,  15,  15)},
                    # Red
                    "red-50" :{"h":"r", "l":50,  "hex":"#FFE1D5", "rgb": (255, 225, 213)},
                    "red-100":{"h":"r", "l":100, "hex":"#FFCABB", "rgb": (255, 202, 187)},
                    "red-150":{"h":"r", "l":150, "hex":"#FDB2A2", "rgb": (253, 178, 162)},
                    "red-200":{"h":"r", "l":200, "hex":"#F89A8A", "rgb": (248, 154, 138)},
                    "red-300":{"h":"r", "l":300, "hex":"#E8705F", "rgb": (232, 112, 95)},
                    "red-400":{"h":"r", "l":400, "hex":"#D14D41", "rgb": (209, 77, 65)},
                    "red-500":{"h":"r", "l":500, "hex":"#C03E35", "rgb": (192, 62, 53)},
                    "red-600":{"h":"r", "l":600, "hex":"#AF3029", "rgb": (175, 48, 41)},
                    "red-700":{"h":"r", "l":700, "hex":"#942822", "rgb": (148, 40, 34)},
                    "red-800":{"h":"r", "l":800, "hex":"#6C201C", "rgb": (108, 32, 28)},
                    "red-850":{"h":"r", "l":850, "hex":"#551B18", "rgb": (85, 27, 24)},
                    "red-900":{"h":"r", "l":900, "hex":"#3E1715", "rgb": (62, 23, 21)},
                    "red-950":{"h":"r", "l":950, "hex":"#261312", "rgb": (38, 19, 18)},
                    # Orange
                    "orange-50": {"h":"o", "l":50,  "hex":"#FFE7CE", "rgb":(255, 231, 206)},
                    "orange-100":{"h":"o", "l":100, "hex":"#FED3AF", "rgb":(254, 211, 175)},
                    "orange-150":{"h":"o", "l":150, "hex":"#FCC192", "rgb":(252, 193, 146)},
                    "orange-200":{"h":"o", "l":200, "hex":"#F9AE77", "rgb":(249, 174, 119)},
                    "orange-300":{"h":"o", "l":300, "hex":"#EC8B49", "rgb":(236, 139, 73)},
                    "orange-400":{"h":"o", "l":400, "hex":"#DA702C", "rgb":(218, 112, 44)},
                    "orange-500":{"h":"o", "l":500, "hex":"#CB6120", "rgb":(203, 97, 32)},
                    "orange-600":{"h":"o", "l":600, "hex":"#BC5215", "rgb":(188, 82, 21)},
                    "orange-700":{"h":"o", "l":700, "hex":"#9D4310", "rgb":(157, 67, 16)},
                    "orange-800":{"h":"o", "l":800, "hex":"#71320D", "rgb":(113, 50, 13)},
                    "orange-850":{"h":"o", "l":850, "hex":"#59290D", "rgb":(89, 41, 13)},
                    "orange-900":{"h":"o", "l":900, "hex":"#40200D", "rgb":(64, 32, 13)},
                    "orange-950":{"h":"o", "l":950, "hex":"#27180E", "rgb":(39, 24, 14)},
                    # Yellow
                    "yellow-50": {"h":"y", "l":50,  "hex":"#FAEEC6", "rgb":(250, 238, 198)},
                    "yellow-100":{"h":"y", "l":100, "hex":"#F6E2A0", "rgb":(246, 226, 160)},
                    "yellow-150":{"h":"y", "l":150, "hex":"#F1D67E", "rgb":(241, 214, 126)},
                    "yellow-200":{"h":"y", "l":200, "hex":"#ECCB60", "rgb":(236, 203, 96)},
                    "yellow-300":{"h":"y", "l":300, "hex":"#DFB431", "rgb":(223, 180, 49)},
                    "yellow-400":{"h":"y", "l":400, "hex":"#D0A215", "rgb":(208, 162, 21)},
                    "yellow-500":{"h":"y", "l":500, "hex":"#BE9207", "rgb":(190, 146, 7)},
                    "yellow-600":{"h":"y", "l":600, "hex":"#AD8301", "rgb":(173, 131, 1)},
                    "yellow-700":{"h":"y", "l":700, "hex":"#8E6B01", "rgb":(142, 107, 1)},
                    "yellow-800":{"h":"y", "l":800, "hex":"#664D01", "rgb":(102, 77, 1)},
                    "yellow-850":{"h":"y", "l":850, "hex":"#503D02", "rgb":(80, 61, 2)},
                    "yellow-900":{"h":"y", "l":900, "hex":"#3A2D04", "rgb":(58, 45, 4)},
                    "yellow-950":{"h":"y", "l":950, "hex":"#241E08", "rgb":(36, 30, 8)},
                    # Green
                    "green-50": {"h":"g", "l":50,  "hex":"#EDEECF", "rgb":(237, 238, 207)},
                    "green-100":{"h":"g", "l":100, "hex":"#DDE2B2", "rgb":(221, 226, 178)},
                    "green-150":{"h":"g", "l":150, "hex":"#CDD597", "rgb":(205, 213, 151)},
                    "green-200":{"h":"g", "l":200, "hex":"#BEC97E", "rgb":(190, 201, 126)},
                    "green-300":{"h":"g", "l":300, "hex":"#A0AF54", "rgb":(160, 175, 84)},
                    "green-400":{"h":"g", "l":400, "hex":"#879A39", "rgb":(135, 154, 57)},
                    "green-500":{"h":"g", "l":500, "hex":"#768D21", "rgb":(118, 141, 33)},
                    "green-600":{"h":"g", "l":600, "hex":"#66800B", "rgb":(102, 128, 11)},
                    "green-700":{"h":"g", "l":700, "hex":"#536907", "rgb":(83, 105, 7)},
                    "green-800":{"h":"g", "l":800, "hex":"#3D4C07", "rgb":(61, 76, 7)},
                    "green-850":{"h":"g", "l":850, "hex":"#313D07", "rgb":(49, 61, 7)},
                    "green-900":{"h":"g", "l":900, "hex":"#252D09", "rgb":(37, 45, 9)},
                    "green-950":{"h":"g", "l":950, "hex":"#1A1E0C", "rgb":(26, 30, 12)},
                    # Cyan
                    "cyan-50": {"h":"c", "l":50,  "hex":"#DDF1E4", "rgb":(221, 241, 228)},
                    "cyan-100":{"h":"c", "l":100, "hex":"#BFE8D9", "rgb":(191, 232, 217)},
                    "cyan-150":{"h":"c", "l":150, "hex":"#A2DECE", "rgb":(162, 222, 206)},
                    "cyan-200":{"h":"c", "l":200, "hex":"#87D3C3", "rgb":(135, 211, 195)},
                    "cyan-300":{"h":"c", "l":300, "hex":"#5ABDAC", "rgb":(90, 189, 172)},
                    "cyan-400":{"h":"c", "l":400, "hex":"#3AA99F", "rgb":(58, 169, 159)},
                    "cyan-500":{"h":"c", "l":500, "hex":"#2F968D", "rgb":(47, 150, 141)},
                    "cyan-600":{"h":"c", "l":600, "hex":"#24837B", "rgb":(36, 131, 123)},
                    "cyan-700":{"h":"c", "l":700, "hex":"#1C6C66", "rgb":(28, 108, 102)},
                    "cyan-800":{"h":"c", "l":800, "hex":"#164F4A", "rgb":(22, 79, 74)},
                    "cyan-850":{"h":"c", "l":850, "hex":"#143F3C", "rgb":(20, 63, 60)},
                    "cyan-900":{"h":"c", "l":900, "hex":"#122F2C", "rgb":(18, 47, 44)},
                    "cyan-950":{"h":"c", "l":950, "hex":"#101F1D", "rgb":(16, 31, 29)},
                    # Blue
                    "blue-50": {"h":"b", "l":50,  "hex":"#E1ECEB", "rgb":(225, 236, 235)},
                    "blue-100":{"h":"b", "l":100, "hex":"#C6DDE8", "rgb":(198, 221, 232)},
                    "blue-150":{"h":"b", "l":150, "hex":"#ABCFE2", "rgb":(171, 207, 226)},
                    "blue-200":{"h":"b", "l":200, "hex":"#92BFDB", "rgb":(146, 191, 219)},
                    "blue-300":{"h":"b", "l":300, "hex":"#66A0C8", "rgb":(102, 160, 200)},
                    "blue-400":{"h":"b", "l":400, "hex":"#4385BE", "rgb":(67, 133, 190)},
                    "blue-500":{"h":"b", "l":500, "hex":"#3171B2", "rgb":(49, 113, 178)},
                    "blue-600":{"h":"b", "l":600, "hex":"#205EA6", "rgb":(32, 94, 166)},
                    "blue-700":{"h":"b", "l":700, "hex":"#1A4F8C", "rgb":(26, 79, 140)},
                    "blue-800":{"h":"b", "l":800, "hex":"#163B66", "rgb":(22, 59, 102)},
                    "blue-850":{"h":"b", "l":850, "hex":"#133051", "rgb":(19, 48, 81)},
                    "blue-900":{"h":"b", "l":900, "hex":"#12253B", "rgb":(18, 37, 59)},
                    "blue-950":{"h":"b", "l":950, "hex":"#101A24", "rgb":(16, 26, 36)},
                    # Purple
                    "purple-50": {"h":"p", "l":50,  "hex":"#F0EAEC", "rgb":(240, 234, 236)},
                    "purple-100":{"h":"p", "l":100, "hex":"#E2D9E9", "rgb":(226, 217, 233)},
                    "purple-150":{"h":"p", "l":150, "hex":"#D3CAE6", "rgb":(211, 202, 230)},
                    "purple-200":{"h":"p", "l":200, "hex":"#C4B9E0", "rgb":(196, 185, 224)},
                    "purple-300":{"h":"p", "l":300, "hex":"#A699D0", "rgb":(166, 153, 208)},
                    "purple-400":{"h":"p", "l":400, "hex":"#8B7EC8", "rgb":(139, 126, 200)},
                    "purple-500":{"h":"p", "l":500, "hex":"#735EB5", "rgb":(115, 94, 181)},
                    "purple-600":{"h":"p", "l":600, "hex":"#5E409D", "rgb":(94, 64, 157)},
                    "purple-700":{"h":"p", "l":700, "hex":"#4F3685", "rgb":(79, 54, 133)},
                    "purple-800":{"h":"p", "l":800, "hex":"#3C2A62", "rgb":(60, 42, 98)},
                    "purple-850":{"h":"p", "l":850, "hex":"#31234E", "rgb":(49, 35, 78)},
                    "purple-900":{"h":"p", "l":900, "hex":"#261C39", "rgb":(38, 28, 57)},
                    "purple-950":{"h":"p", "l":950, "hex":"#1A1623", "rgb":(26, 22, 35)},
                    # Magenta
                    "magenta-50": {"h":"m", "l":50,  "hex":"#FEE4E5", "rgb":(254, 228, 229)},
                    "magenta-100":{"h":"m", "l":100, "hex":"#FCCFDA", "rgb":(252, 207, 218)},
                    "magenta-150":{"h":"m", "l":150, "hex":"#F9B9CF", "rgb":(249, 185, 207)},
                    "magenta-200":{"h":"m", "l":200, "hex":"#F4A4C2", "rgb":(244, 164, 194)},
                    "magenta-300":{"h":"m", "l":300, "hex":"#E47DA8", "rgb":(228, 125, 168)},
                    "magenta-400":{"h":"m", "l":400, "hex":"#CE5D97", "rgb":(206, 93, 151)},
                    "magenta-500":{"h":"m", "l":500, "hex":"#B74583", "rgb":(183, 69, 131)},
                    "magenta-600":{"h":"m", "l":600, "hex":"#A02F6F", "rgb":(160, 47, 111)},
                    "magenta-700":{"h":"m", "l":700, "hex":"#87285E", "rgb":(135, 40, 94)},
                    "magenta-800":{"h":"m", "l":800, "hex":"#641F46", "rgb":(100, 31, 70)},
                    "magenta-850":{"h":"m", "l":850, "hex":"#4F1B39", "rgb":(79, 27, 57)},
                    "magenta-900":{"h":"m", "l":900, "hex":"#39172B", "rgb":(57, 23, 43)},
                    "magenta-950":{"h":"m", "l":950, "hex":"#24131D", "rgb":(36, 19, 29)},
                }
            
                # Each color will also be accessible as an attribute of the Colors class
                # Note here, dashes are replaced with underscores; e.g. colors.dict["red-500"] becomes colors.red_500
                for n,c in self.dict.items():
                    cname = n.lower().replace("-","_")
                    setattr(self, cname, Color(n, **c))
                
                self._update_defaults(400)
                  
            # Convenience function for generating a list of all the Color objects
            def to_list(self):
                return [Color(n, **c) for n,c in self.dict.items()]
            
            # Function to bulk-set the default values (i.e. red, blue, green, etc.)
            def _update_defaults(self, l):
                (self.red, self.orange, self.yellow,
                 self.green, self.cyan, self.blue, 
                 self.purple, self.magenta, self.base) = self.filter("roygcbpmk", l, "h_l", "colors")
            
            # Function to return the default values as a list of Color objects
            # If override_names is set to False, these objects will preserve their names (i.e. red-400, green-600, etc.)
            ## If it is set to True, then the Color names returned will instead be the short versions (i.e. red, green, etc.)
            def get_defaults(self, override_names: bool=False):
                defaults = [self.red, self.orange, self.yellow,
                            self.green, self.cyan, self.blue, 
                            self.purple, self.magenta, self.base]
                if override_names == False:
                    return defaults
                elif override_names == True:
                    names = ["red","orange","yellow","green","cyan","blue","purple","magenta"]
                    if self.base.l == 0:
                        names.append("paper")
                    elif self.base.l == 1000:
                        names.append("black")
                    else:
                        names.append("base")
                    return [Color(n, c.h, c.l, c.hex, c.rgb) for n,c in zip(names,defaults)]
                else:
                    raise Exception(f"Invalid input for override_names: {override_names}; only True or False are accepted, see documentation for details.")
            
            # A function to allow for easy filtering/selection of the colors
            # h is for selecting by hue 
            ## can be either a list of names/letters, a single name/letter, or a single parsed string
            ## the order of the inputs will also be the order in which colors are returned
            ## if None, all hues will be returned (thus, assuming you filtered by lightness instead)
            # l is for selecting by lightness value
            ## can be either a list of integers, a single integer, or a slice of integers
            ## the order of the inputs will also be the order in which the colors are returned
            ## if None, all lightness values will be returned (thus, assuming you filtered by hue instead)
            # order is for determining if the order of the returned colors is organized first by hue or lightness
            ## can be either of the following values: "h_l" (hue, then lightness) or "l_h" (lightness, then hue)
            ## if None, will default to "h_l"
            # returns is for choosing what is returned by the filter function
            ## can be either a Palette object, a list of Color objects, a list of hex codes, a list of rgb values, or a list of rgba values
            ## if None, will default to a Palette or Colors object (depending on if multiple colors are returned, or just one)
            def filter(self, h: List[str] | str=None, l: List[int] | int | slice | range=None, order:Literal["h_l","l_h"]=None, returns:Literal["palette","colors","colours","hexes","rgb","rgba"]=None):
                # Backend function to filter by hue
                def _filter_h(self, h, clist):
                    cfilt = []
                    # Checking if a hue was passed
                    if h is not None:
                        # If h is a single string
                        if isinstance(h, str):
                            h = h.lower()
                            # If h is a single color from the list of color codes, keep it as is
                            if h in h_codes.values():
                                _h = [h]
                            # If h is a single color from the list of color names, convert to its single-letter key
                            elif h in h_codes.keys():
                                _h = [h_codes[h]]
                            # Otherwise try and parse it as an hstring of single color characters
                            else:
                                _h = []
                                for c in h:
                                    if c not in h_codes.values():
                                        raise Exception(f"Invalid input for h: {c}; only valid colors are shortcodes are accepted, see documentation for details.")    
                                    else:
                                        _h.append(c)

                        # If h is a list of some sort
                        elif isinstance(h, (tuple, list, Iterable)):
                            h = [c.lower() for c in h]
                            _h = []
                            for c in h:
                                # Making sure it is a valid string
                                if not isinstance(c, str) or not c.lower() in h_codes.values() or not c.lower() in h_codes.keys():
                                    raise Exception(f"Invalid input for h: {c}; only valid colors are shortcodes are accepted, see documentation for details.")
                                # Converting the string based on what type of code it is, and appending to our eventual list
                                c = c.lower()
                                # If it is a single-letter code
                                if c in h_codes.values():
                                    _h.append(c)
                                # If it is a full color name
                                elif c in h_codes.keys():
                                    _h.append(h_codes[c])
                                # If it is neither of these things, raise an error
                                else:
                                    raise Exception(f"Invalid input for h: {c}; only valid colors are shortcodes are accepted, see documentation for details.")
                                
                        # If none of these things, raise an exception
                        else:
                            raise Exception(f"Invalid input for h: {h}; only valid colors are shortcodes are accepted, see documentation for details.")
                        
                        # Once all the above are finished processing, should have a list of color codes that we can then use to filter the main color list like so:
                        for hue in _h:
                            # Custom filter for when base is selected; don't want to return base-0/base-1000, instead return paper/black
                            if hue == "k":
                                cfilt += [c for c in clist if c.h==hue and not (c.name=="base-0" or c.name=="base-1000")]
                            # Otherwise, appending colors that match the hue to our list
                            else:
                                cfilt += [c for c in clist if c.h==hue]
                    # Alternatively, if None is passed, then no filtering is needed
                    else:
                        cfilt = clist
                    # Returning the filtered list
                    return cfilt
                
                # Backend function to filter by lightness
                def _filter_l(self, l, clist):
                    cfilt = []
                    # Getting all the lightness values
                    l_all = [l for l in l_values]
                    # Checking if a lightness is passed
                    if l is not None:
                        # If l is a single integer
                        if isinstance(l, int):
                            # Convert into a list
                            _l = [l]

                        # If l is a list of some sort
                        elif isinstance(l, (tuple, list, Iterable)):
                            _l = []
                            for k in l:
                                # Making sure it is a valid integer
                                if not isinstance(k, int) or not k in l_values:
                                    raise Exception(f"Invalid input for l: {k}; only valid lightness values are accepted, see documentation for details.")
                                else:
                                    _l.append(l)
                        # If l is a slice instead
                        elif isinstance(l, (slice, range)):
                            # Extracting the values
                            l_min, l_max = sorted([l.start, l.stop])
                            # Reversing the order if need be
                            if l.start > l.stop:
                                l_all.reverse()
                            # Keeping just the lightness values that fall within the range
                            _l = [l for l in l_all if l>=l_min and l<=l_max]
                        # If none of these things, raise an exception
                        else:
                            raise Exception(f"Invalid input for l: {l}; only valid lightness values are accepted, see documentation for details.")
                        
                        # Once all the above are finished processing, should have a list of color codes that we can then use to filter the main color list like so:
                        for light in _l:
                            # Custom filter for when paper/base-0 is selected; need to only return one of them
                            if light == 0:
                                cfilt += [self.paper]
                            # Similar filter for when black/base-1000 is selected
                            elif light == 1000:
                                cfilt += [self.black]
                            # Otherwise, appending colors that match the lightness to our list
                            else:
                                cfilt += [c for c in clist if c.l==light]
                    # Alternatively, if None is passed, then no filtering is needed
                    else:
                        cfilt = clist
                    # Returning the filtered list
                    return cfilt

                # The list that will ultimately be filtered
                colors_all = self.to_list()
                # Running the filters, based on order
                if order is None or order == "h_l":
                    colors_filtered = _filter_h(self, h, _filter_l(self, l, colors_all))
                elif order == "l_h":
                    colors_filtered = _filter_l(self, l, _filter_h(self, h, colors_all))
                else:
                    raise Exception(f"Invalid input for order: {order}; only 'h_l' and 'l_h' are acceptable values, see documentation for details.")
                
                # Deciding what to return
                if len(colors_filtered) == 0:
                    raise Exception(f"No colors returned for selected filters (h={h}, l={l}).")
                elif returns is None:
                    if len(colors_filtered) == 1:
                        return colors_filtered[0]
                    else:
                        return Palette(colors_filtered)
                elif returns == "palette":
                    return Palette(colors_filtered)
                elif returns == "colors" or returns == "colours":
                    return colors_filtered
                elif returns == "hexes":
                    return [c.hex for c in colors_filtered]
                elif returns == "rgb":
                    return [c.rgb for c in colors_filtered]
                elif returns == "rgba":
                    return [c.rgba for c in colors_filtered]
                else:
                    raise Exception(f"Invalid input for returns: {returns}; only 'palette', 'colors', 'colours, 'hexes', 'rgb', or 'rgba' are acceptable values, see documentation for details.")
        
        self.colors = colors()

        # This class will handle all the palettes (collections of colors)
        class palettes:
            # The colors class needs to be passed here, as the filter function is necessary during the set-up
            def __init__(self, colors, l):
                # Initializing all the monochromatic palettes - single color, every lightness value
                self.grays = colors.filter("k", None)
                self.blacks = colors.filter("k", None)
                self.whites = colors.filter("k", None)
                self.base = colors.filter("k", None)

                self.reds = colors.filter("r", None)
                self.oranges = colors.filter("o", None)
                self.yellows = colors.filter("y", None)
                self.greens = colors.filter("g", None)
                self.cyans = colors.filter("c", None)
                self.blues = colors.filter("b", None)
                self.purples = colors.filter("p", None)
                self.magentas = colors.filter("m", None)

                # Initializing all the monolightness palettes - single lightness value, every color
                self.l50  = colors.filter(None, 50)
                self.l100 = colors.filter(None, 100)
                self.l150 = colors.filter(None, 150)
                self.l200 = colors.filter(None, 200)
                self.l300 = colors.filter(None, 300)
                self.l400 = colors.filter(None, 400)
                self.l500 = colors.filter(None, 500)
                self.l600 = colors.filter(None, 600)
                self.l700 = colors.filter(None, 700)
                self.l800 = colors.filter(None, 800)
                self.l850 = colors.filter(None, 850)
                self.l900 = colors.filter(None, 900)
                self.l950 = colors.filter(None, 950)

                # Finally, initializing a special palette called "defaults"
                # which will contain the monolightness palette for the current theme/lightness color chosen
                self._defaults = Palette(colors.get_defaults(override_names=False))
            
            # Setting up the defaults palette so that it can be updated
            @property
            def defaults(self):
                return self._defaults
            
            @defaults.setter
            def defaults(self, p):
                if not isinstance(p, Palette):
                    raise Exception("Invalid value passed to palettes.defaults; only Palette objects can be used. Note that defaults should not be set directly by the user - it is automatically set when the lightness/theme values are changed.")
                else:
                    self._defaults = p

        self.palettes = palettes(self.colors, self._lightness)

    # Creating the properties for lightness, and how they will update the other colors
    @property
    def lightness(self):
        return self._lightness

    @lightness.setter
    def lightness(self, l):
        if l is None:
            raise Exception(f"Invalid input for lightness: {l}; the only accepted values are {l_values[1:-1]}.")
        elif l in l_values[1:-1]:
            self._lightness = l
            # Setting the appropriate theme too, if needed
            if l == 400:
                self._theme = "light"
            elif l == 600:
                self._theme = "dark"
            else:
                self._theme = None
            # This is the step to reset all the defaults
            self.colors._update_defaults(l)
            self.palettes.defaults = Palette(self.colors.get_defaults(override_names=False))
        else:
            raise Exception(f"Invalid input for lightness: {l}; the only accepted values are {l_values[1:-1]}.")
    
    # Creating the properties for theme, and how they will update the other colors
    @property
    def theme(self):
        if self._theme is not None:
            return self._theme
        else:
            print(f"No theme set; current lightness value is {self._lightness}")

    @theme.setter
    def theme(self, t):
        if t is None:
            raise Exception(f"Invalid input for theme: {t}; only 'light' and 'dark' are accepted values.")
        elif t.lower() == "light":
            self._theme = t.lower()
            self.lightness = 400
        elif t.lower() == "dark":
            self._theme = t.lower()
            self.lightness = 600
        else:
            raise Exception(f"Invalid input for theme: {t}; only 'light' and 'dark' are accepted values.")


    # Creating a more convenient way to access the filter function: so you can use Flexoki.filter() instead of Flexoki.colors.filter()
    def filter(self, h: List[str] | str=None, l: List[int] | int | slice=None, order:Literal["h_l","l_h"]=None, returns:Literal["palette","colors","colours","hexes","rgb","rgba"]=None):
        return self.colors.filter(h, l, order, returns)

    # Creating methods for changing the lightness values of the default colors
    def set_lightness(self, lightness: int):
        self.lightness = lightness

    # Lightness values for default colors can also be set via the "theme"
    def set_theme(self, theme: Literal["light","dark"]):
        self.theme = theme
    
    # Function to register colors with matplotlib, so they are callable within matplotlib plot() functions via strings
    # colors needs to be a list of either dicts, Colors, lists, or tuples
    ## If dicts are passed, they need two keys: "name" (what the name of the color should be, excepting the prefix) and "color" (either the hex code or the RGBA values)
    ## If colors are passed, name and hex are used from their attributes
    ## If lists or tuples are passed, they need two values: the first should be the name, the second the color value
    ## If no colors are passed, then it will register all the colors available under self.colors
    # prefix is the string that will be prepended to the name for each color
    ## A colon will be inserted to separate the prefix from the name, which can help prevent overwriting default names
    ## Ex. for "red" with a prefix of "flexoki", the full color name is "flexoki:red"
    # defaults is a boolean variable telling the function whether to register the default/theme colors as well
    ## Note that this is ONLY used if no color list is passed! (colors = None)
    ## Otherwise it is silently ignored
    def register_matplotlib(self, colors:List[dict | Color | list | tuple]=None, prefix:str="flexoki", defaults:bool=True):
        # First, if colors is None, getting the full list of colors we have
        if colors is None:
            colors = self.colors.to_list()
            if defaults == True:
                colors += self.colors.get_defaults(override_names=True)
        # Then making sure a prefix was passed
        if prefix is None or not isinstance(prefix, str):
            raise Exception(f"Invalid input for prefix - must be a valid string; see documentation for details.")
        # Then, checking that a list of colors was passed
        if not isinstance(colors, (list, tuple)):
            raise Exception(f"Invalid input for colors - must be a list of dicts, Colors, or lists or tuples (of length 2); see documentation for details.")
        else:
            # Storing the eventual list of colors we need to update
            added_colors = {}
            # Iterating though what was passed; doing it this way allows for mixing of types
            for c in colors:
                # Colors
                if isinstance(c, Color):
                    added_colors[f"{prefix}:{c.name}"] = c.color
                # Dictionaries
                elif isinstance(c, dict):
                    # Checking for keys
                    if "name" in c.keys() and "color" in c.keys():
                        added_colors[f"{prefix}:{c["name"]}"] = c["color"]
                    else:
                        raise Exception(f"Invalid input for colors: {c}; dictionaries must have two keys in them, 'name' and 'color'; see documentation for details.")
                # Lists/Tuples
                elif isinstance(c, (list, tuple)):
                    if len(c) > 1 and isinstance(c[0], str):
                        added_colors[f"{prefix}:{c[0]}"] = c[1]
                    else:
                        raise Exception(f"Invalid input for colors: {c}; lists and tuples must be of length 2, where 'name' corresponds to the first entry and 'color to the second; see documentation for details.")
            # Once complete, register the colors
            # from https://stackoverflow.com/questions/76886019/create-new-named-color-in-matplotlib
            matplotlib.colors.get_named_colors_mapping().update(added_colors)