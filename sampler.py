# -*- encoding: utf-8 -*-
'''
@File    :   sampler.py
@Time    :   2019/05/21 15:18:56
@Author  :   Painter
@Contact :   painter9509@126.com

          ❤❤❤❤❤❤      ❤❤❤❤❤❤
        ❤          ❤  ❤         ❤
      ❤             ❤❤            ❤
     ❤                              ❤
     ❤       ====  ====  =||        ❤
     ❤      ||        ||  ||        ❤
      ❤      ====  ====   ||       ❤
        ❤       ||||      ||     ❤
          ❤  ====  ====  ====  ❤
            ❤                ❤
              ❤            ❤
                ❤        ❤
                  ❤❤❤❤❤

'''


import os
import argparse
import random
import shutil
import yaml

from config import cfg


def update_cfg():
    parser = argparse.ArgumentParser(description="Sampling Dataset")
    parser.add_argument(
        "dataset", type=str,
        help="The name of dataset. The related YAML file which has the same filename must exist.")
    parser.add_argument(
        "dest_dir", type=str,
        help="The destination directory where saves samples. The directory will be created, if does not exist.")
    parser.add_argument(
        "splits", type=str,
        help="Split must be included in `train`, `val` and `test`. If more splits are needed, use `,` (in English) to connect them, such as `train&val&test`. `trainval` is equivalent to `train,val`. Both uppercase and lowercase are valid.")
    parser.add_argument(
        "sample_sizes", type=str,
        help="More sizes of sample can be connected by `,` (in English), such as `7,3`. The order is corresponding to `splits`'s.")
    parser.add_argument(
        "--method", type=str, choices=["RANDOM", "SEQUENTIAL"],
        default="RANDOM",
        help="The method of sampling. As the name, `RANDOM` and `SEQUENTIAL` are available. Default is `RANDOM`.")
    args = parser.parse_args()

    # Read YAML file.
    BASICPATH = os.path.dirname(os.path.abspath(__file__))
    config_files_dir = os.path.join(BASICPATH, "configs")
    config_fnames = os.listdir(config_files_dir)
    config_fname = args.dataset.lower() + ".yaml"
    if config_fname not in config_fnames:
        raise Exception("Invalid dataset - " + args.dataset)

    config_file_path = os.path.join(config_files_dir, config_fname)
    with open(config_file_path, 'r', encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    src_dir = os.path.abspath(config["src_dir"])
    src_split_files_dir = os.path.abspath(config["src_split_files_dir"])
    valid_splits = config["valid_splits"]
    targets = config["targets"]

    # Get splits and sample sizes.
    splits = [split.strip() for split in args.splits.split(',')]
    sample_sizes = [int(sample_size.strip())
        for sample_size in args.sample_sizes.split(',')]

    # Check illegal parameters.
    if len(splits) != len(sample_sizes):
        raise Exception("Illegal parameter `splits` or `sample_sizes`.",
            "The length of them should be euqal.")
    for split in splits:
        if split not in valid_splits:
            raise Exception("Illegal split - " + split)

    # Update `cfg`.
    dest_dir = os.path.abspath(args.dest_dir)
    kwargs = {
        "src_dir": src_dir,
        "dest_dir": dest_dir,
        "src_split_files_dir": src_split_files_dir,
        "splits": splits,
        "targets": targets,
        "sample_sizes": sample_sizes,
        "method": args.method
    }
    cfg.update(kwargs)


def get_splits_sample_ids():
    splits_sample_ids = {}
    for split, sample_size in zip(cfg.splits, cfg.sample_sizes):
        src_split_file_path = os.path.join(cfg.src_split_files_dir, split + ".txt")
        with open(src_split_file_path, 'r') as f:
            ids = [int(idx.strip()) for idx in f.readlines()]
        
        if sample_size > len(ids):
            raise Exception(
                "The Sample size `{}` of `{}` is out of maximun.".format(
                    sample_size, split))

        if cfg.method == "RANDOM":
            sample_ids = random.sample(ids, sample_size)
        elif cfg.method == "SEQUENTIAL":
            sample_ids = ids[: sample_size]
        else:
            raise Exception("Illegal method: " + cfg.method)

        splits_sample_ids[split] = sample_ids
    
    return splits_sample_ids


def copy_targets(split, sample_ids):
    for target_dir, target_ext in cfg.targets.items():
        src_target_file_path = os.path.join(
            cfg.src_dir, target_dir, "{:0>6}." + target_ext)

        dest_target_file_dir = os.path.join(cfg.dest_dir, target_dir)
        if not os.path.exists(dest_target_file_dir):
            os.makedirs(dest_target_file_dir)

        dest_target_file_path = os.path.join(
            dest_target_file_dir, "{:0>6}." + target_ext)

        for idx in sample_ids:
            shutil.copy(
                src_target_file_path.format(idx),
                dest_target_file_path.format(idx))

    print("Successfully sample {} data for split {}.".format(
        len(sample_ids), split))

   
def update_split_file(split, sample_ids):
    dest_split_file_path = os.path.join(cfg.dest_dir, split + ".txt")

    if os.path.exists(dest_split_file_path):
        print("Already exist destination file: {}.".format(
            dest_split_file_path))
        print("Updating ...")
        # Merge the old and new.
        with open(dest_split_file_path, 'r') as f:
            existed_ids = [int(existed_id.strip())
                for existed_id in f.readlines()]
            sample_ids = set(existed_ids + sample_ids)

    sample_ids = ["{:0>6}".format(sample_id) for sample_id in sample_ids]
    sample_ids_str = "\n".join(sample_ids)
    with open(dest_split_file_path, 'w') as f:
        f.write(sample_ids_str)
    
    print(
        "Successfully generate/update split file {}.txt".format(split),
        "containing {} items.".format(len(sample_ids)))


def update_trainval():
    dest_train_split_file_path = os.path.join(cfg.dest_dir, "train.txt")
    dest_val_split_file_path = os.path.join(cfg.dest_dir, "val.txt")
    if os.path.exists(dest_train_split_file_path) and \
        os.path.exists(dest_val_split_file_path):
        ids = []
        for dest_split_file_path in \
            [dest_train_split_file_path, dest_val_split_file_path]:
            with open(dest_split_file_path, 'r') as f:
                ids += [int(idx.strip()) for idx in f.readlines()]
        ids = set(ids)

        ids = ["{:0>6}".format(idx) for idx in ids]
        ids_str = "\n".join(ids)
        dest_trainval_split_file_path = os.path.join(
            cfg.dest_dir, "trainval.txt")
        with open(dest_trainval_split_file_path, 'w') as f:
            f.write(ids_str)

        print(
            "Sucessfully generate/update split file trainval.txt",
            "containing {} items.".format(len(ids)))
        
        
def main():
    update_cfg()

    splits_sample_ids = get_splits_sample_ids()

    maybe_trainval = False
    for split, sample_ids in splits_sample_ids.items():
        copy_targets(split, sample_ids)
        update_split_file(split, sample_ids)
        if split in ["train", "val"]:
            maybe_trainval = True
    
    if maybe_trainval:
        update_trainval()

    print("Sample successfully.")


if __name__ == "__main__":
    main()