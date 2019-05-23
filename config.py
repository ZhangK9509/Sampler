# -*- encoding: utf-8 -*-
'''
@File    :   config.py
@Time    :   2019/05/22 15:05:08
@Author  :   Painter
@Contact :   painter9509@126.com

          ❤❤❤❤❤❤      ❤❤❤❤❤❤
        ❤          ❤  ❤         ❤
      ❤             ❤❤            ❤
     ❤          ღ        ღ          ❤
     ❤        ღ     ღღ     ღ        ❤
     ❤      ღ  0x522 = 1314  ღ      ❤
      ❤        ღ          ღ        ❤
        ❤         ღ    ღ         ❤
          ❤         ღღ        ❤
            ❤                ❤
              ❤            ❤
                ❤        ❤
                  ❤❤❤❤❤

'''

class Config(object):
    def __init__(self):
        super(Config, self).__init__()
        self.src_dir = ""
        self.dest_dir = ""
        self.src_split_files_dir = ""
        self.splits = []
        self.targets = {}
        self.sample_sizes = []
        self.method = "RANDOM"

    def update(self, *new_cfg):
        state_dict = vars(self)
        for kwargs in new_cfg:
            for k, v in kwargs.items():
                if k not in state_dict:
                    continue
                setattr(self, k, v)

        print("====== user config ======")
        for k, v in vars(self).items():
            print("{}: {}".format(k, v))
        print("======     end     ======\n")


cfg = Config()