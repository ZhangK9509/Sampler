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
        self.__src_dir = ""
        self.__src_split_files_dir = ""
        self.__dest_dir = ""
        self.__dest_split_files_dir = ""
        self.__splits = []
        self.__targets = {}
        self.__sample_sizes = []
        self.__method = "RANDOM"

    def get_src_dir(self):
        return self.__src_dir

    def get_src_split_files_dir(self):
        return self.__src_split_files_dir
    
    def get_dest_dir(self):
        return self.__dest_dir

    def get_dest_split_files_dir(self):
        return self.__dest_split_files_dir

    def get_splits(self):
        return self.__splits

    def get_targets(self):
        return self.__targets

    def get_sample_sizes(self):
        return self.__sample_sizes

    def get_method(self):
        return self.__method
        
    def update(self, *new_cfg):
        state_dict = vars(self)
        for kwargs in new_cfg:
            for k, v in kwargs.items():
                k = "_{}__{}".format(self.__class__.__name__, k)
                if k not in state_dict:
                    continue
                setattr(self, k, v)

        print("====== user config ======")
        for k, v in vars(self).items():
            print("{}: {}".format(k, v))
        print("======     end     ======\n")


cfg = Config()