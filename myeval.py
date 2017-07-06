"""
This script should be run from root directory of this codebase:
https://github.com/tylin/coco-caption
"""
import matplotlib
matplotlib.use('AGG')
import sys
import argparse
from config import config
arg_parser = argparse.ArgumentParser(description='')
arg_parser.add_argument('input_json', type=str, help='Produced Captions')
arg_parser.add_argument('annFile', nargs='?', default=config.ALL_ANN_FILE, type=str,
                        help='Gold Captions')
args=arg_parser.parse_args()
sys.path.append(".")
from pycocotools.coco import COCO
from pycocoevalcap.eval import COCOEvalCap
import json
coco = COCO(args.annFile)
valids = coco.getImgIds()
cocoRes = coco.loadRes(args.input_json)
cocoEval = COCOEvalCap(coco, cocoRes)
cocoEval.params['image_id'] = cocoRes.getImgIds()
cocoEval.evaluate()

# create output dictionary
out = dict(cocoEval.eval)

# serialize to file, to be read from Lua
json.dump(out, open(args.input_json + '_out.json', 'w'))
