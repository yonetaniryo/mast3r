import mast3r.utils.path_to_dust3r  # noqa

from dust3r.image_pairs import make_pairs
from dust3r.utils.image import load_images

from mast3r.cloud_opt import sparse_ga

from glob import glob
from mast3r.model import AsymmetricMASt3R
import os
import sys

from logging import getLogger


logger = getLogger(__name__)


def main(input_directory: str):
    model = AsymmetricMASt3R.from_pretrained(
        "naver/MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric"
    )
    cache_dir = "cache"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    filelist = glob(os.path.join(input_directory, "*.jpg"))
    imgs = load_images(filelist, size=224, verbose=False)
    pairs = make_pairs(imgs, prefilter=None, symmetrize=True)

    scene = sparse_ga.sparse_global_alignment(
        filelist,
        pairs,
        cache_dir,
        model,
        device="cpu",
        opt_depth=False,
        shared_intrinsics=True,
    )
    logger.info(scene.cam2w)


if __name__ == "__main__":
    input_directory = sys.argv[1]
    main(input_directory)
