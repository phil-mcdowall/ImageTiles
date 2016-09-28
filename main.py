import os
import argparse
from PIL import Image, ImageDraw



class TiledImage():
    def __init__(self, path, tile_dim, outpath=None, target_overlap=0):
        assert(len(tile_dim) == 2)
        assert(0 <= target_overlap <= 1)
        self.img = Image.open(path)
        self.height = self.img.width
        self.width = self.img.height
        self.ncol = tile_dim[1]
        self.nrow = tile_dim[0]
        self.baseDir = os.path.dirname(path)
        self.name = os.path.basename(path)
        self.tiles = []
        self.overlap = target_overlap
        if outpath:
            self.outPath = outpath
        else:
            self.outPath = self.baseDir
        self.tileScheme = self.generate_tile_scheme()
        self.tileSchemeCache = None
        print "Initialising"

    def generate_tile_scheme(self):
        print "Generating tile scheme"
        self.tile_width = self.width/self.ncol
        self.tile_height = self.height/self.nrow
        for i in xrange(self.ncol):
            for j in xrange(self.nrow):
                left = int(i*self.tile_height)
                upper = int(j*self.tile_width)
                right = int(i*self.tile_height + self.tile_height*(1+self.overlap))
                lower = int(j*self.tile_width + self.tile_width*(1+self.overlap))
                yield (left,upper,right,lower)

    def show_tile_scheme(self):
        if self.tileSchemeCache:
            self.tileSchemeCache.show()
        else:
            self.generate_tile_scheme_cache()
            self.tileSchemeCache.show()

    def generate_tile_scheme_cache(self):
        imgcpy = self.img.copy()
        draw = ImageDraw.Draw(imgcpy)
        for tile in self.tileScheme:
            draw.rectangle(tile, outline=(200, 0, 0))
            # draw.rectangle(base_rect, outline=(0, 0, 0))
            draw.text(tuple(x + 10 for x in tile[0:2]), str(tile), fill=(0, 0, 0))
        self.tileSchemeCache = imgcpy

    def export_tile_scheme_cache(self):
        if self.tileSchemeCache:
            self.tileSchemeCache.save(os.path.join(self.outPath,"tileScheme.jpg"))
        else:
            self.generate_tile_scheme_cache()
            self.tileSchemeCache.save(os.path.join(self.outPath,"tileScheme.jpg"))

    def tile(self):
        self.export_tile_scheme_cache()
        for tile in self.generate_tile_scheme():
            self.create_tile(tile)

    def check_bbox(self, bbox):
        assert(len(bbox)==4)

    def gen_tile_name(self,bbox):
        return "_".join(map(str,bbox)) + "_" + self.name

    def create_tile(self, bbox):
        self.check_bbox(bbox)
        #PIL origin at top left
        tile = self.img.crop(bbox)
        tilename = self.gen_tile_name(bbox)
        tile.save(os.path.join(self.outPath,tilename))

    def __repr__(self):
        return str(self.img) + '\n' + str(self.tiles)


if __name__ ==  "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","-path",help="Path of image to be tiled")
    parser.add_argument("-c","-ncol",help="Number of columns")
    parser.add_argument("-r","-nrow", help="Number of rows")
    args = parser.parse_args()
    print args
    tileimg = TiledImage(args.p, (int(args.c), int(args.r)))
    tileimg.tile()


